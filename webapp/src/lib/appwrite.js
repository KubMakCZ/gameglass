import { Client, Databases, Storage, Account } from 'appwrite';

const client = new Client();
client
    .setEndpoint(import.meta.env.VITE_APPWRITE_ENDPOINT || 'http://172.26.37.54/v1')
    .setProject(import.meta.env.VITE_APPWRITE_PROJECT_ID || ''); 

export const account = new Account(client);
export const databases = new Databases(client);
export const storage = new Storage(client);

// Konstanty
export const DB_ID = 'gameglass_db';
export const COLLECTION_ID = 'games';
export const BUCKET_ZIPS_ID = 'games_zips';

export default client;
