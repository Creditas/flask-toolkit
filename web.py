from flask_toolkit.application import create_application


app = create_application(
    config=dict(
        DEBUG=True
    )
)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
