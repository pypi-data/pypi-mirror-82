'''
Server code for setting up a WebSocket server, handling connections, and verifying
connection details. The class `Server` is what is used to run the project.

Required 3rd-party libraries:
`autobahn`
`twisted`

Info on connecting to the server:
The path part of the url should be of the format:
    /gameID/name/token/...     <- reconnect
    /gameID/name/null/...      <- first connect

Everything after the fourth slash is ignored by the server code
and passed directly to the `joinPlayer` method of `AbstractGame`,
as the otherRequestData argument.

The server also sends the json string {'token': <token> }.
This token should be kept as it is used to identify the player
and allow them to rejoin a game if they get disconnected.
'''
import sys
import json
from typing import Callable, Dict, Optional
import re

from twisted.python import log, logfile # type: ignore
from twisted.internet import reactor, ssl, task # type: ignore

from .factoryAndProtocol import _ServerFactory, _ServerProtocol
from .tokenStorage import TokenStorage, BasicTokenStorage
from ..requestProcessor import interactions, RequestProcessor
from ..requestProcessor.game import AbstractTimeGame


class Server:

    def __init__(self, ip: Optional[str], port: Optional[int], 
            requestProcessor: RequestProcessor,
            playerTokenStorage: TokenStorage = BasicTokenStorage(),
            config: Optional[Dict[str, object]] = None
            ):
        '''
        A class for managing the code for running the server.
        To setup the server, run `s = Server()`,
        and then run `s.run()` to start it.

        If config is None, it will look for a config.json file.
        If neither the argument nor file exists, it will
        raise an Exception.

        Config options are:
        USE_SSL: bool,
        verbose: bool,
        key: str,
        cert: str,
        ip: str,
        port: int,
        printAllOutgoing: bool -> Print all data sent out

        verbose defaults to False if not found
        printAllOutgoing defaults to False if not found
        key & cert are only needed if USE_SSL==True
        ip & port are only needed if the respective arguments are None
        '''
        assert isinstance(requestProcessor, RequestProcessor)
        assert isinstance(playerTokenStorage, TokenStorage)

        if config is None:
            config = self.__getConfig()


        tmp = config['USE_SSL']
        assert isinstance(tmp, bool)
        USE_SSL: bool = tmp

        verbose: bool
        if 'verbose' in config:
            tmp = config['verbose']
            assert isinstance(tmp, bool)
            verbose = tmp
        else:
            verbose = False
        
        printAllOutgoing: bool
        if 'printAllOutgoing' in config:
            tmp = config['printAllOutgoing']
            assert isinstance(tmp, bool)
            printAllOutgoing = tmp
        else:
            printAllOutgoing = False
        
        if ip is None:
            tmp = None
            if 'IP' in config:
                tmp = config['IP']
                if not isinstance(tmp, str):
                    raise TypeError(f'IP found in config is not a str, but type "{type(tmp)}"')

            elif 'ip' in config:
                tmp = config['ip']
                if not isinstance(tmp, str):
                    raise TypeError(f'IP found in config is not a str, but type "{type(tmp)}"')

            
            if tmp is None:
                raise ValueError("IP not given as argument and also not found in config")
            ip = tmp
            del tmp
        
        if port is None:
            tmp = None
            if 'port' in config:
                tmp = config['port']
                if not isinstance(tmp, int):
                    raise TypeError(f'Port number found in config is not an int, but type "{type(tmp)}"')

            if tmp is None:
                raise ValueError("Port not given as argument and also not found in config")
            port = tmp


        regex = r'([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})|localhost'

        if re.fullmatch(regex, ip) is None:
            raise ValueError(f'Invalid ip: {ip}')

        self.ip: str = ip
        self.port: int = port

        self.__requestProcessor: RequestProcessor = requestProcessor

        self.logFile = open('gameMsgLog.log', 'w')

        protocol = 'ws'

        self.contextFactory: Optional[ssl.DefaultOpenSSLContextFactory] = None
        if USE_SSL:
            protocol = 'wss'
            key = config['key']
            cert = config['cert']
            assert isinstance(key, str)
            assert isinstance(cert, str)
            self.contextFactory = ssl.DefaultOpenSSLContextFactory(key, cert)

        # Setup server factory
        self.server = _ServerFactory(
            u'{}://{}:{}'.format(protocol, ip, port), 
            self.logFile, 
            serverCallback=self.callback,
            tokenDataStorage=playerTokenStorage,
            playerDB=self.__requestProcessor.playerDatabase,
            verbose=verbose,
            printAllOutgoing=printAllOutgoing
            )

        self.server.protocol = _ServerProtocol

        print(f'WebSocket server on {self.ip}:{self.port}')

        if USE_SSL:
            reactor.listenSSL(self.port, self.server, self.contextFactory) # pylint: disable=no-member
        else:
            # setup listening server
            reactor.listenTCP(self.port, self.server) # pylint: disable=no-member

    @staticmethod
    def __getConfig() -> Dict[str, object]:
        data = None
        try:
            f = open('config.json')
            data = f.read()
            f.close()
        except FileNotFoundError as e:
            print('Could not find config file: {e}. Either provide a config.json or pass it in')
            raise

        return json.loads(data)

    def callback(self, re: interactions.UnprocessedClientRequest) -> interactions.Response:
        '''
        Handles messages from players
        '''
        return self.__requestProcessor.process(re)

    def run(self, serverLogFilename: str = 'twistedLog.log', 
                  timeout: Optional[float] = None,
                  callOnTimer: Optional[Callable[[], None]] = None):
        '''
        Run the server. This method will not return
        until the server is ended by an Exception like ^C.

        Timeout is useful when actions need to be triggered
        on a timer, with timout being a float representing
        the seconds between calls.
        If `callOnTimer` is set, it will be called every time
        the timer triggers. Additionally, any game implementing
        the `AbstractTimeGame` will have its `onTimer` method
        be called.
        '''
        log.startLogging(sys.stdout, setStdout=True)

        logFile = logfile.LogFile.fromFullPath(serverLogFilename)
        log.addObserver(log.FileLogObserver(logFile).emit)

        if callOnTimer is not None and not callable(callOnTimer):
            raise TypeError(f'Func specified, but it is not callable: "{type(callOnTimer)}"')

        def loopCall() -> None:
            if callOnTimer:
                callOnTimer()

            gDB = self.__requestProcessor.gameDatabase
            gameIDs = gDB.getAllGameIDs()
            for gID in gameIDs:
                game = gDB.getGame(gID)
                if game and isinstance(game, AbstractTimeGame):
                    result = game.onTimer()
                    if result is None:
                        continue
                    if isinstance(result, interactions.TimerResponse):
                        self.server.handleTimerResponse(result)
                    else:
                        raise TypeError(f'Method onTimer did not return Optional[ResponseSuccess] but instead "{type(result)}" in game "{type(game)}"')

                        

        try:
            if timeout:
                loop = task.LoopingCall(loopCall)
                loop.start(timeout)

            # start listening for and handling connections
            reactor.run() # pylint: disable=no-member
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
        finally:
            self.logFile.close()
            # if logs are sent to a file instead of stdout
            # the file should be closed here with f.close()
