Polydojo KB
===========

Intentionally simple Knowledge Base (KB) software, to help your users help themselves.

Quickstart
----------

For installing and running **locally**, please follow these steps:

1. Clone the repo: `git clone https://github.com/polydojo/polydojo_kb.git`
2. Change into it: `cd polydojo_kb`
3. Install backend dependencies: `pip install -r requirements.txt`
4. Install frontend dependencies: `npm install`
5. Copy the env-config template (for dev): `cp env-example.txt env-dev.txt`
6. Edit `env-dev.txt`, specify (or replace) *at least* the following:
    - `DATABASE_URL`: Full MongoDB (or soon, Postgres) connection string.
    - `SECRET_KEY`: A secure, randomly generated, secret token.
7. Bundle frontend code: `npx webpack`
8. Run backend app: `python appRun.py env-dev.txt`
9. Visit http://localhost:8880/setup to set up the first user!

Quick Notes:
- For hot reloads use:
    - Frontend: `npx webpack --watch`
    - Backend: `hupper -m appRun env-dev.txt`
- To securely generate a random secret via the Python REPL, use:
    - `>>> import secrets; print(secrets.token_urlsafe())`

Nascent Stage
-------------

Polydojo KB is being developed by the folks at [Polydojo, Inc.](https://www.polydojo.com/), led by [Sumukh Barve](https://www.sumukhbarve.com/). The project is currently in a nascent stage. As work progresses, we'll be adding docs, features, and much more.

Licensing
---------
Copyright (c) 2021 Polydojo, Inc.

**Software Licensing:**  
The software is released "AS IS" under the **GNU AGPLv3** (version 3 only), WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Kindly see [LICENSE.txt](https://github.com/polydojo/polydojo_kb/blob/master/LICENSE.txt) for more details.

**No Trademark Rights:**  
The above software licensing terms **do not** grant any right in the trademarks, service marks, brand names or logos of Polydojo, Inc.
