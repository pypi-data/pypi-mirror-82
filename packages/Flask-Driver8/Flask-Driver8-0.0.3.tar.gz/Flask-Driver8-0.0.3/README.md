# Driver8: WireProtocol support for Python Flask apps

## Installation

Use it as [Blueprint](https://flask.palletsprojects.com/en/1.1.x/tutorial/views/?highlight=blueprint) in your Flask 
application:

    ```python
    from flask_driver8 import driver8_blueprint
    
    app = Flask(__name__)
    app.register_blueprint(driver8_blueprint.driver8_blueprint)
    
    if __name__ == "__main__":
       app.run(host='0.0.0.0', debug=True, port=80)
    ```
    