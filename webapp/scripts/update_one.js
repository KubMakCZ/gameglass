import fs from 'fs';
import path from 'path';
import { Client, Databases, Storage, ID, Query } from 'node-appwrite';
import { InputFile } from 'node-appwrite/file';
import dotenv from 'dotenv';

dotenv.config();

const APPWRITE_ENDPOINT = process.env.VITE_APPWRITE_ENDPOINT || 'http://localhost/v1';
const APPWRITE_PROJECT_ID = process.env.VITE_APPWRITE_PROJECT_ID;
const APPWRITE_API_KEY = process.env.APPWRITE_API_KEY;

const client = new Client()
    .setEndpoint(APPWRITE_ENDPOINT)
    .setProject(APPWRITE_PROJECT_ID)
    .setKey(APPWRITE_API_KEY);

const databases = new Databases(client);
const storage = new Storage(client);

const DB_ID = 'gameglass_db';
const COLLECTION_ID = 'games';
const BUCKET_ZIPS_ID = 'games_zips';

async function fixGame() {
    console.log("Hledám hru Vanesy...");
    const docs = await databases.listDocuments(DB_ID, COLLECTION_ID, [
        Query.equal('author', 'Nekvasilová Vanesa')
    ]);
    
    if (docs.documents.length === 0) {
        console.log("Hra nenalezena v databázi!");
        return;
    }
    
    const gameDoc = docs.documents[0];
    console.log("Nalezena hra:", gameDoc.title, "ID:", gameDoc.$id);
    
    // Smazeme stary zip
    try {
        if (gameDoc.zip_file_id) {
            await storage.deleteFile(BUCKET_ZIPS_ID, gameDoc.zip_file_id);
            console.log("Smazán starý ZIP ze storage");
        }
    } catch(e) { console.log("Chyba při mazání starého ZIPu", e.message); }
    
    // Nahrajeme novy zip
    const zipPath = 'C:/gitprojekty/gameglass/studenti/1im/Nekvasilová_Vanesa/hotovo.zip';
    const newFile = await storage.createFile(
        BUCKET_ZIPS_ID,
        ID.unique(),
        InputFile.fromPath(zipPath, `hra_Nekvasilova_Vanesa.zip`)
    );
    console.log("Nahrán nový ZIP:", newFile.$id);
    
    // Aktualizujeme zaznam
    await databases.updateDocument(DB_ID, COLLECTION_ID, gameDoc.$id, {
        zip_file_id: newFile.$id
    });
    
    console.log("Hotovo! Hra by měla fungovat.");
}

fixGame();
