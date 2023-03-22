from src import create_app


app = create_app()


from uvicorn import run


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=5000, reload=True)
