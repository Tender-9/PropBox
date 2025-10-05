from propbox._data_manager import DataManager
from propbox._module import Module
from flask import Flask, jsonify
from threading import Thread

class Api(Module):
    def __init__(self, data_manager:DataManager, host="0.0.0.0", port=8000) -> None:
        super().__init__()
        self._data_manager = data_manager
        self._host = host
        self._port = port
        self._app = None
        self._server_thread = None
        
    def start(self, period:float=1, offset:float=0):
        if self._server_thread and self._server_thread.is_alive():
            return
        
        self._setup_app()
        self._server_thread = Thread(target=self._run_server, daemon=True)
        self._server_thread.start()
        print(f"🚀 API server starting on http://{self._host}:{self._port}")
    
    def _setup_app(self):
        self._app = Flask(__name__)
        
        @self._app.route("/status")
        def get_status():
            return jsonify(self._data_manager.as_dict())
        
        @self._app.route("/health")
        def health():
            return jsonify({"status": "ok"})
    
    def _run_server(self):
        try:
            self._app.run(
                host=self._host,
                port=self._port,
                debug=False,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            print(f"API server error: {e}")
    
    def _update(self):
        # Not used since we override start(), but required by Module ABC
        pass
    
    def stop(self):
        print("Stopping API server...")
        super().stop()
