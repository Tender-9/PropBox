from flask import Flask, jsonify, render_template_string
import threading

class Gui():
    def __init__(self, data_manager, host="0.0.0.0", port=5000):
        self.data_manager = data_manager
        self.host = host
        self.port = port
        self.app = Flask(__name__)

        @self.app.route("/")
        def index():
            return render_template_string(self._html_template())

        @self.app.route("/latest")
        def latest():
            return jsonify(self._get_latest())

    def _get_latest(self):
        return self.data_manager.as_dict()

    def _html_template(self):
        return """

<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PropBox</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      
      body {
        font-family: 'Courier New', Courier, monospace;
        background: #f8f9fa;
        color: #1a1a1a;
        min-height: 100vh;
        padding: 1.5rem;
      }
      
      .container {
        max-width: 1400px;
        margin: 0 auto;
      }
      
      header {
        border-bottom: 2px solid #1a1a1a;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
      }
      
      h1 {
        font-size: clamp(1.5rem, 4vw, 2rem);
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #1a1a1a;
        text-transform: uppercase;
      }
      
      .status {
        margin-top: 0.5rem;
        font-size: 0.875rem;
        color: #666;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }
      
      .status-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        background: #1a1a1a;
        border-radius: 50%;
        margin-right: 6px;
        animation: blink 2s infinite;
      }
      
      @keyframes blink {
        0%, 49%, 100% { opacity: 1; }
        50%, 99% { opacity: 0.3; }
      }
      
      .timestamp {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }
      
      .timestamp-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
      }
      
      .timestamp-value {
        font-size: clamp(1.25rem, 3vw, 1.5rem);
        color: #1a1a1a;
        font-weight: 600;
      }
      
      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
      }
      
      .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1.5rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        transition: border-color 0.2s;
      }
      
      .metric-card:hover {
        border-color: #a0a0a0;
      }
      
      .metric-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
        font-weight: 600;
      }
      
      .metric-value {
        font-size: clamp(2.5rem, 6vw, 3.5rem);
        color: #1a1a1a;
        font-weight: 300;
        line-height: 1;
        margin-bottom: 0.5rem;
        font-family: 'Courier New', Courier, monospace;
      }
      
      .metric-unit {
        font-size: 1.25rem;
        color: #666;
        font-weight: 400;
        margin-left: 0.25rem;
      }
      
      .metric-range {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e8e8e8;
        font-size: 0.875rem;
        color: #666;
        display: flex;
        justify-content: space-between;
      }
      
      .range-item {
        display: flex;
        flex-direction: column;
      }
      
      .range-label {
        font-size: 0.7rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
      }
      
      .range-value {
        color: #1a1a1a;
        font-weight: 600;
      }
      
      .loading {
        text-align: center;
        padding: 3rem;
        color: #666;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }
      
      @media (max-width: 768px) {
        body {
          padding: 1rem;
        }
        
        header {
          margin-bottom: 1.5rem;
        }
        
        .grid {
          gap: 1rem;
          grid-template-columns: 1fr;
        }
        
        .metric-card {
          padding: 1.25rem;
        }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <header>
        <h1>PropBox</h1>
        <div class="status" id="status">
          <span class="status-dot"></span>
          Last Update: Loading...
        </div>
      </header>
      
      <div class="grid" id="data">
        <div class="loading">Initializing system...</div>
      </div>
    </div>

    <script>
      function formatValue(val, decimals = 1) {
        return val != null ? val.toFixed(decimals) : '--';
      }
      
      function formatRPM(val) {
        return val != null ? Math.round(val) : '--';
      }
      
      async function refresh() {
        try {
          const res = await fetch("/latest");
          const d = await res.json();
          
          document.getElementById("status").innerHTML = `
            <span class="status-dot"></span>
            Last Update: ${d.time || '--'}
          `;
          
          document.getElementById("data").innerHTML = `
            <div class="metric-card">
              <div class="metric-label">Temperature</div>
              <div class="metric-value">
                ${formatValue(d.temperature)}
                <span class="metric-unit">°C</span>
              </div>
              ${d.min_temperature != null && d.max_temperature != null ? `
                <div class="metric-range">
                  <div class="range-item">
                    <span class="range-label">Minimum</span>
                    <span class="range-value">${d.min_temperature} °C</span>
                  </div>
                  <div class="range-item">
                    <span class="range-label">Maximum</span>
                    <span class="range-value">${d.max_temperature} °C</span>
                  </div>
                </div>
              ` : ''}
            </div>
            
            <div class="metric-card">
              <div class="metric-label">Relative Humidity</div>
              <div class="metric-value">
                ${formatValue(d.humidity)}
                <span class="metric-unit">%</span>
              </div>
              ${d.min_humidity != null && d.max_humidity != null ? `
                <div class="metric-range">
                  <div class="range-item">
                    <span class="range-label">Minimum</span>
                    <span class="range-value">${d.min_humidity} %</span>
                  </div>
                  <div class="range-item">
                    <span class="range-label">Maximum</span>
                    <span class="range-value">${d.max_humidity} %</span>
                  </div>
                </div>
              ` : ''}
            </div>
            
            <div class="metric-card">
              <div class="metric-label">Fan PWM Setting</div>
              <div class="metric-value">
                ${d.fan_pwm != null ? d.fan_pwm : '--'}
                <span class="metric-unit">%</span>
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-label">Fan Speed</div>
              <div class="metric-value">
                ${formatRPM(d.fan_rpm)}
                <span class="metric-unit">RPM</span>
              </div>
            </div>
          `;
        } catch (err) {
          console.error('Failed to fetch data:', err);
          document.getElementById("data").innerHTML = `
            <div class="loading">Connection error. Retrying...</div>
          `;
        }
      }
      
      setInterval(refresh, 1000);
      refresh();
    </script>
  </body>
</html>
"""

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        self.app.run(host=self.host, port=self.port)
