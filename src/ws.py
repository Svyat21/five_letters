import typing
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket
from .five_letter import FiveLetterGame


class WSGame(WebSocketEndpoint):
    encoding = 'json'
    actions = ['create', 'game']
    game = None

    async def create_game(self, ws: WebSocket) -> None:
        game = await FiveLetterGame.create()
        self.game = game

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
    
    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        if data['action'] in self.actions:
            if data['action'] == 'create':
                await self.create_game(websocket)
                await websocket.send_json({'words': self.game.any_word()})
            if data['action'] == 'game':
                if self.game:
                    await websocket.send_json({'words': self.game.run(data['data'])})
    
    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        if self.game:
            del self.game
        await super().on_disconnect(websocket, close_code)
