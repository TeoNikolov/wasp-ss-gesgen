# Copyright 2023 by Teodor Nikolov.
# All rights reserved.
# This file is part of the WASP Summer School 2023 Gesture Generation Application,
# and is released under the GPLv3 License. Please see the LICENSE
# file that should have been included as part of this package.

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
	return {"Hello": "World"}
