const FLIPPED_DIRECTION = {
    U: "D",
    L: "R",
    D: "U",
    R: "L",
};
const COLUMN = 6;
const OBSTACLE = 6;
const { Game } = require("./game");

const cookie = `sessionid=${process.env.JUEJIN_SESSION_ID};`;
const findPath = (map) => {
    const mapTrack = [
        [3, 1, "U"],
        [2, 2, "L"],
        [4, 2, "D"],
        [3, 3, "R"],
    ];

    // Convert 1D array to 2D
    const map2d = [];
    map.map((item, index) => {
        if (index % COLUMN == 0) {
            map2d.push([item]);
        } else {
            map2d[map2d.length - 1].push(item);
        }
    });

    // Filter out obstacles
    const trackXY = mapTrack.filter((item) => {
        const xy = map2d[item[0]][item[1]];
        return xy !== OBSTACLE;
    });

    // Travel back to the initial position
    const trackList = trackXY
        .map((item) => {
            return [item[2], FLIPPED_DIRECTION[item[2]]];
        })
        .flat();
    return trackList;
};

let n = 0;
const autoGame = async () => {
    n++;
    if (n > 500) return; // Prevent infinite loops
    let exp = new Game(cookie);
    let gameData = await exp.openGame();
    if (gameData === undefined)
        throw "Failed on startup due to unknown reasons";
    if (!gameData) return;

    const { mapData } = gameData;
    const track = findPath(mapData);
    exp.move(track).then(() => {
        exp.outGame().then(async (res) => {
            res.body = JSON.parse(res.body);
            console.log(
                `Game ${n} --> reward: ${res.body.data.realDiamond}, accumulated: ${res.body.data.todayDiamond}, limit: ${res.body.data.todayLimitDiamond}`
            );

            if (res.body.data.realDiamond < 40) {
                // reward < 40, not worthy to continue, refresh the map
                await exp.refreshMap();
            }
            // reward < limit, continue
            if (res.body.data.todayDiamond < res.body.data.todayLimitDiamond) {
                setTimeout(() => {
                    autoGame();
                }, 1000);
            } else {
                return;
            }
        });
    });
};

autoGame();
