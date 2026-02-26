const { spawn } = require("child_process");
const { ActivityHandler, MessageFactory } = require("botbuilder");
const { verifyAdmin, Admin } = require("./db/database");

class SecurityBot extends ActivityHandler {
    constructor() {
        super();

        this.onMessage(async (context, next) => {
            if (!context || !context.sendActivity) {
                console.error("❌ Bot execution context does not exist.");
                return;
            }

            const userMessage = context.activity.text.toLowerCase();
            const userId = context.activity.from.id;
            const password = context.activity.from.name; // Simulated password input

            // Authenticate admin using MongoDB
            const isAdmin = await verifyAdmin(userId, password);
            if (!isAdmin) {
                await context.sendActivity(MessageFactory.text("❌ Access Denied: Invalid admin credentials."));
                return;
            }

            // Execute bot commands
            if (userMessage.includes("install patches")) {
                await this.runPowerShell(context, "scripts/installSecurityPatch.ps1", "⚙️ Installing security patches...");
            } else if (userMessage.includes("monitor logs")) {
                await this.runPowerShell(context, "scripts/monitorLogs.ps1", "📊 Monitoring security logs...");
            } else if (userMessage.includes("update antivirus")) {
                await this.runPowerShell(context, "scripts/updateAntivirus.ps1", "🔄 Updating antivirus...");
            } else if (userMessage.includes("scan vulnerabilities")) {
                await this.runPowerShell(context, "scripts/scanVulnerabilities.ps1", "🔍 Scanning for vulnerabilities...");
            } else if (userMessage.includes("fetch logs")) {
                await this.fetchLogs(context);
            } else if (userMessage.includes("add admin")) {
                await this.addAdmin(context, userMessage);
            } else {
                await context.sendActivity(MessageFactory.text("🤖 I can perform security tasks! Try 'install patches', 'monitor logs', or 'update antivirus'."));
            }

            await next();
        });
    }

    async addAdmin(context, userMessage) {
        const [_, newAdminId, newPassword] = userMessage.split(" "); // Example: "add admin deepak_admin secure123"
        if (!newAdminId || !newPassword) {
            await context.sendActivity(MessageFactory.text("❌ Incorrect format. Use 'add admin <admin_id> <password>'"));
            return;
        }

        const admin = new Admin({ admin_id: newAdminId, password: newPassword });
        await admin.save();
        await context.sendActivity(MessageFactory.text(`✅ New admin '${newAdminId}' added successfully!`));
    }

    async runPowerShell(context, scriptPath, initialMessage) {
        try {
            await context.sendActivity(MessageFactory.text(initialMessage));

            const childProcess = spawn("powershell.exe", ["-ExecutionPolicy", "Bypass", "-File", scriptPath], { shell: true });

            let finalOutput = "";

            childProcess.stdout.on("data", (data) => {
                finalOutput += `🛡️ Security Logs:\n${data.toString().trim()}\n`;
            });

            childProcess.stderr.on("data", (data) => {
                finalOutput += `⚠️ PowerShell Error:\n${data.toString().trim()}\n`;
            });

            childProcess.on("close", async () => {
                await context.sendActivity(MessageFactory.text(finalOutput));
            });

        } catch (err) {
            console.error("❌ Unexpected Error:", err);
        }
    }
}

module.exports.SecurityBot = SecurityBot;