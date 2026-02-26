const restify = require("restify");
const { BotFrameworkAdapter } = require("botbuilder");
const { SecurityBot } = require("./bot");

const adapter = new BotFrameworkAdapter({
    onTurnError: async (context, error) => {
        console.error(`❌ Bot Error: ${error}`);
        await context.sendActivity("⚠️ Oops! Something went wrong.");
    }
});

const bot = new SecurityBot();

const server = restify.createServer();
server.use(restify.plugins.bodyParser());

server.post("/api/messages", async (req, res) => {
    try {
        await adapter.processActivity(req, res, async (context) => {
            await bot.run(context);
        });

        if (!res.headersSent) {
            res.send(200, "✅ Message processed successfully");
        }
    } catch (err) {
        console.error("❌ Error processing bot request:", err);
        if (!res.headersSent) {
            res.send(500, "⚠️ Internal Server Error");
        }
    }
});

server.listen(3978, () => {
    console.log("🚀 Security Bot is running on http://localhost:3978");
});