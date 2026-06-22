import fs from 'fs';
import path from 'path';
import { Client, Databases, Storage, ID, Query } from 'node-appwrite';
import { InputFile } from 'node-appwrite/file';
import dotenv from 'dotenv';

dotenv.config();

const client = new Client()
    .setEndpoint(process.env.VITE_APPWRITE_ENDPOINT || 'http://localhost/v1')
    .setProject(process.env.VITE_APPWRITE_PROJECT_ID)
    .setKey(process.env.APPWRITE_API_KEY);

const databases = new Databases(client);
const storage = new Storage(client);

const DB_ID = 'gameglass_db';
const COLLECTION_ID = 'games';
const BUCKET_ZIPS_ID = 'games_zips';

async function updateGame(authorName, zipPath) {
    console.log(`Hledám hru: ${authorName}...`);
    const docs = await databases.listDocuments(DB_ID, COLLECTION_ID, [
        Query.equal('author', authorName)
    ]);
    
    if (docs.documents.length === 0) {
        console.log(`Hra od ${authorName} nenalezena!`);
        return;
    }
    
    const gameDoc = docs.documents[0];
    
    if (gameDoc.zip_file_id) {
        try {
            await storage.deleteFile(BUCKET_ZIPS_ID, gameDoc.zip_file_id);
            console.log(`Smazán starý ZIP ze storage pro ${authorName}`);
        } catch(e) {}
    }
    
    const newFile = await storage.createFile(
        BUCKET_ZIPS_ID,
        ID.unique(),
        InputFile.fromPath(zipPath, `hra_${authorName.replace(' ', '_')}.zip`)
    );
    console.log(`Nahrán nový ZIP pro ${authorName}: ${newFile.$id}`);
    
    await databases.updateDocument(DB_ID, COLLECTION_ID, gameDoc.$id, {
        zip_file_id: newFile.$id
    });
}

async function run() {
    await updateGame('Kovářík Jindřich', 'C:/gitprojekty/gameglass/studenti/1im/Kovářík_Jindřich/hotovo.zip');
    await updateGame('Ševčík Karel', 'C:/gitprojekty/gameglass/studenti/1im/Ševčík_Karel/hotovo.zip');
    console.log("Hotovo!");
}

run();
