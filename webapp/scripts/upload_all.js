import fs from 'fs';
import path from 'path';
import { Client, Databases, Storage, ID } from 'node-appwrite';
import { InputFile } from 'node-appwrite/file';
import dotenv from 'dotenv';

// Načtení .env z webapp složky
dotenv.config();

const APPWRITE_ENDPOINT = process.env.VITE_APPWRITE_ENDPOINT || 'http://localhost/v1';
const APPWRITE_PROJECT_ID = process.env.VITE_APPWRITE_PROJECT_ID;
const APPWRITE_API_KEY = process.env.APPWRITE_API_KEY;

if (!APPWRITE_PROJECT_ID || !APPWRITE_API_KEY) {
    console.error('Chybí .env proměnné!');
    process.exit(1);
}

const client = new Client()
    .setEndpoint(APPWRITE_ENDPOINT)
    .setProject(APPWRITE_PROJECT_ID)
    .setKey(APPWRITE_API_KEY);

const databases = new Databases(client);
const storage = new Storage(client);

const DB_ID = 'gameglass_db';
const COLLECTION_ID = 'games';
const BUCKET_ZIPS_ID = 'games_zips';

const BASE_DIR = "C:/gitprojekty/gameglass/studenti";

async function uploadStudentGames() {
    for (const cls of ['1i', '1im']) {
        const clsPath = path.join(BASE_DIR, cls);
        if (!fs.existsSync(clsPath)) continue;
        
        for (const student of fs.readdirSync(clsPath)) {
            const studentDir = path.join(clsPath, student);
            if (!fs.statSync(studentDir).isDirectory()) continue;
            
            const metaPath = path.join(studentDir, 'metadata.json');
            const zipPath = path.join(studentDir, 'hotovo.zip');
            
            if (fs.existsSync(metaPath) && fs.existsSync(zipPath)) {
                try {
                    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
                    console.log(`Nahrávám hru: ${meta.title} od ${meta.author}`);
                    
                    // Nahrání ZIPu
                    const file = await storage.createFile(
                        BUCKET_ZIPS_ID,
                        ID.unique(),
                        InputFile.fromPath(zipPath, `hra_${student}.zip`)
                    );
                    
                    // Uložení do DB
                    await databases.createDocument(DB_ID, COLLECTION_ID, ID.unique(), {
                        title: meta.title,
                        author: meta.author,
                        type: meta.type,
                        zip_file_id: file.$id,
                        git_url: '' // Nema
                    });
                    
                    console.log(`✅ Úspěšně nahráno: ${meta.title}`);
                } catch (err) {
                    console.error(`❌ Chyba u studenta ${student}:`, err.message);
                }
            }
        }
    }
}

uploadStudentGames().then(() => console.log('Dokončeno!'));
