const got = require("got");
const jwt = require("jsonwebtoken");

const GET_TOKEN_URL = "https://juejin.cn/get/token";
const HEADER = {
    "user-agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
};

const HOST_BASE = "https://juejin-game.bytedance.com/game/sea-gold";
const START_GAME_URL = HOST_BASE + "/game/start?";
const LOGIN_GAME_URL = HOST_BASE + "/user/login?";
const GET_INFO_URL = HOST_BASE + "/home/info?";
const COMMAND_URL = HOST_BASE + "/game/command?";
const GAME_OVER_URL = HOST_BASE + "/game/over?";
const REFRESH_MAP_URL = HOST_BASE + "/game/fresh_map?";
const ROLE_LIST = {
    YOYO: 1,
    CLICK: 2,
    HAWKING: 3,
};

const PUBLIC_KEY = `-----BEGIN EC PARAMETERS-----
BggqhkjOPQMBBw==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIDB7KMVQd+eeKt7AwDMMUaT7DE3Sl0Mto3LEojnEkRiAoAoGCCqGSM49
AwEHoUQDQgAEEkViJDU8lYJUenS6IxPlvFJtUCDNF0c/F/cX07KCweC4Q/nOKsoU
nYJsb4O8lMqNXaI1j16OmXk9CkcQQXbzfg==
-----END EC PRIVATE KEY-----
`;

class Game {
    #uid;
    #username;
    #cookie;
    #authorization;
    #gameId;

    constructor(cookie) {
        this.#cookie = cookie;
    }

    // Get authorized
    #getToken = () => {
        const cookie = this.#cookie;
        return got.post(GET_TOKEN_URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            cookie,
                        });
                    },
                ],
            },
        });
    };

    // Get UID i.e. profile ID
    #getUid = () => {
        const URL = "https://api.juejin.cn/user_api/v1/user/profile_id";
        const authorization = this.#authorization;
        const cookie = this.#cookie;
        return got.get(URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            cookie,
                        });
                    },
                ],
            },
        });
    };

    // Get user info
    #getInfo = () => {
        const URL =
            GET_INFO_URL + `uid=${this.#uid}&time=` + new Date().getTime();
        const authorization = this.#authorization;
        return got.get(URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            authorization: authorization,
                        });
                    },
                ],
            },
        });
    };

    // Login
    #loginGame = () => {
        const URL =
            LOGIN_GAME_URL + `uid=${this.#uid}&time=` + new Date().getTime();
        const body = { name: this.#username };
        const authorization = this.#authorization;
        return got.post(URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            authorization: authorization,
                        });
                    },
                ],
            },
            json: body,
        });
    };

    // Start the game
    #startGame = (roleId) => {
        const URL =
            START_GAME_URL + `uid=${this.#uid}&time=` + new Date().getTime();
        const body = { roleId };
        const authorization = this.#authorization;
        return got.post(URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            authorization: authorization,
                        });
                    },
                ],
            },
            json: body,
        });
    };

    // Move the character
    // Example: "1 step up, 6 steps right" is represented as
    // {"command":["U", {"times":6,"command":["R"]}]}
    move = (command) => {
        const NOW_TIME = new Date().getTime();
        const URL = COMMAND_URL + `uid=${this.#uid}&time=` + NOW_TIME;
        const body = { command };
        const authorization = this.#authorization;
        const xttgameid = this.#getSign(NOW_TIME);
        return got.post(URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            authorization: authorization,
                            "x-tt-gameid": xttgameid,
                        });
                    },
                ],
            },
            json: body,
        });
    };

    // Calculate sign, parameter t = current timestamp (13-digits)
    #getSign = (t) => {
        return jwt.sign(
            {
                gameId: this.#gameId,
                time: t,
            },
            PUBLIC_KEY,
            {
                algorithm: "ES256",
                expiresIn: 2592e3,
                header: {
                    alg: "ES256",
                    typ: "JWT",
                },
            }
        );
    };

    // End the game
    outGame = () => {
        const URL =
            GAME_OVER_URL + `uid=${this.#uid}&time=` + new Date().getTime();
        const body = { isButton: 1 };
        const authorization = this.#authorization;
        return got.post(URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            authorization: authorization,
                        });
                    },
                ],
            },
            json: body,
        });
    };

    // Refresh and get a new map
    refreshMap = () => {
        const URL =
            REFRESH_MAP_URL + `uid=${this.#uid}&time=` + new Date().getTime();
        const body = {};
        const authorization = this.#authorization;
        return got.post(URL, {
            hooks: {
                beforeRequest: [
                    (options) => {
                        Object.assign(options.headers, {
                            ...HEADER,
                            authorization: authorization,
                        });
                    },
                ],
            },
            json: body,
        });
    };

    // Start a new game (main entrance of this class)
    openGame = async () => {
        // 1. Get authorized
        let res = await this.#getToken().json();
        this.#authorization = "Bearer " + res.data;

	// 2. Get UID
        res = await this.#getUid().json()
        this.#uid = res.data.profile_id;

        // 3. Get username
        res = await this.#getInfo().json();
        this.#username = res.data.userInfo.name;
        const gameStatus = res.data.gameStatus;

        // 4. Login
        await this.#loginGame().json();

        if (gameStatus !== 0) {
            // Log out first if it's currently logged in
            await this.outGame();
        }

        // 5. Start the game and get the game ID
        res = await this.#startGame(ROLE_LIST.CLICK).json();
        this.#gameId = res.data.gameId;

        // 6. Return data
        return this.#gameId !== undefined ? res.data : undefined;
    };
}

exports.Game = Game;
