from flask import Flask, request, jsonify, render_template
from simulang_lexer import tokenize
from simulang_parser import parse
from simulang_interpreter import execute, Environment
import io
import sys
import os
import threading

app = Flask(__name__)

# Global execution state
runner_thread = None
stop_flag = False
output_buffer = io.StringIO()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compile", methods=["POST"])
def compile_code():
    code = request.json.get("code", "")
    try:
        tokens = tokenize(code)
        ast = parse(tokens)
        return jsonify({"output": f"Compilation successful.\\nAST: {repr(ast)}"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/run", methods=["POST"])
def run_code():
    global runner_thread, stop_flag, output_buffer

    code = request.json.get("code", "")
    stop_flag = False
    output_buffer = io.StringIO()

    def run():
        global stop_flag
        try:
            tokens = tokenize(code)
            ast = parse(tokens)
            env = Environment()
            sys.stdout = output_buffer
            for node in ast.children:
                execute(node, env, lambda: not stop_flag)
        except Exception as e:
            output_buffer.write("Error: " + str(e))
        finally:
            sys.stdout = sys.__stdout__

    runner_thread = threading.Thread(target=run)
    runner_thread.start()

    return jsonify({"output": "Execution started."})

@app.route("/stop", methods=["POST"])
def stop_execution():
    global stop_flag
    stop_flag = True
    return jsonify({"status": "Execution stop requested."})

@app.route("/fetch_output", methods=["GET"])
def fetch_output():
    global runner_thread
    is_alive = runner_thread.is_alive() if runner_thread else False
    return jsonify({
        "output": output_buffer.getvalue(),
        "done": not is_alive
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)