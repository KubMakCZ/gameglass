import fs from 'fs';
import path from 'path';
import { ZipArchive } from 'archiver';
import { Client, Databases, Storage, ID, Permission, Role } from 'node-appwrite';
import { InputFile } from 'node-appwrite/file';
import dotenv from 'dotenv';

// Načtení .env souboru
dotenv.config();

const APPWRITE_ENDPOINT = process.env.VITE_APPWRITE_ENDPOINT || 'http://localhost/v1';
const APPWRITE_PROJECT_ID = process.env.VITE_APPWRITE_PROJECT_ID;
const APPWRITE_API_KEY = process.env.APPWRITE_API_KEY;

// Cesta k tvému repozitáři s ukázkovými hrami
const EXAMPLES_DIR = 'C:/gitprojekty_skola/python_gamejam_examples';

if (!APPWRITE_PROJECT_ID || !APPWRITE_API_KEY) {
    console.error('❌ Chybí APPWRITE_PROJECT_ID nebo APPWRITE_API_KEY v .env souboru!');
    console.error('   Vytvoř soubor .env ve složce webapp a vlož do něj tyto proměnné.');
    process.exit(1);
}

// Inicializace Server SDK (má plná práva na tvorbu databází atd.)
const client = new Client()
    .setEndpoint(APPWRITE_ENDPOINT)
    .setProject(APPWRITE_PROJECT_ID)
    .setKey(APPWRITE_API_KEY);

const databases = new Databases(client);
const storage = new Storage(client);

// Konstanty IDček
const DB_ID = 'gameglass_db';
const COLLECTION_ID = 'games';
const BUCKET_ZIPS_ID = 'games_zips';

// Pomocná funkce pro zazipování specifických souborů/složek
function zipSpecificPaths(pathsToZip, outPath, rootPath) {
    return new Promise((resolve, reject) => {
        const archive = new ZipArchive({ zlib: { level: 9 } });
        const stream = fs.createWriteStream(outPath);
        
        archive.on('error', err => reject(err));
        stream.on('close', () => resolve());
        archive.pipe(stream);

        for (const itemPath of pathsToZip) {
            const fullPath = path.join(rootPath, itemPath);
            if (!fs.existsSync(fullPath)) continue;

            const stat = fs.statSync(fullPath);
            if (stat.isDirectory()) {
                const dirName = path.basename(itemPath);
                archive.directory(fullPath, dirName);
            } else {
                archive.file(fullPath, { name: path.basename(itemPath) });
            }
        }
        
        archive.finalize();
    });
}

const anyPermissions = [
    Permission.read(Role.any()),
    Permission.create(Role.any()),
    Permission.update(Role.any()),
    Permission.delete(Role.any())
];

async function setupAppwrite() {
    console.log('🚀 Inicializuji strukturu Appwrite...');

    // 1. Storage Bucket
    try {
        await storage.getBucket(BUCKET_ZIPS_ID);
        console.log('✅ Bucket "games_zips" už existuje. Zvyšuji jeho povolenou velikost na 500 MB...');
        await storage.updateBucket(BUCKET_ZIPS_ID, 'Games ZIPs', anyPermissions, undefined, undefined, 500000000);
    } catch {
        console.log('📦 Vytvářím bucket "games_zips" s limitem 500 MB...');
        await storage.createBucket(BUCKET_ZIPS_ID, 'Games ZIPs', anyPermissions, undefined, undefined, 500000000);
    }

    // 2. Databáze
    try {
        await databases.get(DB_ID);
        console.log('✅ Databáze "gameglass_db" už existuje.');
    } catch {
        console.log('🗄️ Vytvářím databázi "gameglass_db"...');
        await databases.create(DB_ID, 'GameGlass DB');
    }

    // 3. Kolekce a Atributy
    try {
        await databases.getCollection(DB_ID, COLLECTION_ID);
        console.log('✅ Kolekce "games" už existuje.');
    } catch {
        console.log('🗂️ Vytvářím kolekci "games"...');
        await databases.createCollection(DB_ID, COLLECTION_ID, 'Games', anyPermissions);
        
        console.log('📝 Přidávám atributy do tabulky (počkám 3 vteřiny na propsání)...');
        await databases.createStringAttribute(DB_ID, COLLECTION_ID, 'title', 255, true);
        await databases.createStringAttribute(DB_ID, COLLECTION_ID, 'author', 255, true);
        await databases.createStringAttribute(DB_ID, COLLECTION_ID, 'type', 50, true);
        await databases.createStringAttribute(DB_ID, COLLECTION_ID, 'zip_file_id', 255, true);
        
        // Appwrite vytváří atributy asynchronně, je dobré chvíli počkat
        await new Promise(res => setTimeout(res, 3000));
    }
}

async function cleanupAppwrite() {
    console.log('\n🧹 Čistím předchozí data (promazávám databázi a storage)...');
    try {
        const docs = await databases.listDocuments(DB_ID, COLLECTION_ID);
        for (const doc of docs.documents) {
            await databases.deleteDocument(DB_ID, COLLECTION_ID, doc.$id);
        }
        
        const files = await storage.listFiles(BUCKET_ZIPS_ID);
        for (const file of files.files) {
            await storage.deleteFile(BUCKET_ZIPS_ID, file.$id);
        }
        console.log('✅ Stará data smazána!');
    } catch (e) {
        console.log('Nebyl nalezen žádný starý obsah k promazání.');
    }
}

async function seedGames() {
    await cleanupAppwrite();

    const gamesToSeed = [
        { 
            id: 'py_obesenec', title: 'Obešenec', author: 'Učitel IT', type: 'python', 
            paths: ['pure_python/01_obesenec.py'] 
        },
        { 
            id: 'py_textovka', title: 'Textová hra', author: 'Učitel IT', type: 'python', 
            paths: ['pure_python/02_textova_hra.py'] 
        },
        { 
            id: 'pg_pexeso', title: 'Pexeso', author: 'Učitel IT', type: 'pygame', 
            paths: ['pygame/01_pexeso.py', 'pygame/assets'] 
        },
        { 
            id: 'pg_flappy', title: 'Flappy Bird', author: 'Učitel IT', type: 'pygame', 
            paths: ['pygame/02_flappy_bird.py', 'pygame/assets'] 
        },
        { 
            id: 'renpy_1', title: 'RenPy Visual Novel', author: 'Učitel IT', type: 'renpy', 
            paths: ['renpy/renpy_example_01'] 
        }
    ];

    const tempDir = path.join(process.cwd(), 'temp_zips');
    if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir);

    for (const game of gamesToSeed) {
        const zipPath = path.join(tempDir, `${game.id}.zip`);
        
        console.log(`\n📦 Zabaluji ${game.title}...`);
        await zipSpecificPaths(game.paths, zipPath, EXAMPLES_DIR);
        
        console.log(`☁️ Nahrávám do Appwrite Storage...`);
        const file = await storage.createFile(
            BUCKET_ZIPS_ID, 
            ID.unique(), 
            InputFile.fromPath(zipPath, `${game.title.replace(/ /g, '_')}.zip`)
        );

        console.log(`💾 Ukládám do databáze her...`);
        await databases.createDocument(DB_ID, COLLECTION_ID, ID.unique(), {
            title: game.title,
            author: game.author,
            type: game.type,
            zip_file_id: file.$id
        });

        console.log(`✅ ${game.title} úspěšně zpracována!`);
    }
    
    console.log('\n🎉 Vše hotovo! Databáze byla promazána a nově naplněna správnými hrami.');
}

async function main() {
    try {
        await setupAppwrite();
        await seedGames();
    } catch (e) {
        console.error('❌ Chyba běhu skriptu:', e.message);
    }
}

main();
