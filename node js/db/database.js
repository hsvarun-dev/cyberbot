const mongoose = require("mongoose");
require("dotenv").config();

const mongoURI = process.env.MONGO_URI;

if (!mongoURI) {
    console.error("❌ MongoDB connection URI is missing! Set MONGO_URI in .env file.");
    process.exit(1);
}

// Fix: Remove deprecated options
mongoose.connect(mongoURI);

const db = mongoose.connection;
db.on("error", console.error.bind(console, "❌ Connection Error:"));
db.once("open", () => console.log("✅ Connected to MongoDB!"));

const adminSchema = new mongoose.Schema({
    admin_id: String,
    password: String,
});

const Admin = mongoose.model("Admin", adminSchema);

async function verifyAdmin(userId, password) {
    const admin = await Admin.findOne({ admin_id: userId, password: password });
    return admin !== null;
}

module.exports = { Admin, verifyAdmin };