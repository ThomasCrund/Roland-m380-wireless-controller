import { io } from 'socket.io-client';

// "undefined" means the URL will be computed from the `window.location` object
const URL = process.env.NODE_ENV === 'production' ? undefined : window.location.protocol + "//" + window.location.host.substring(0, window.location.host.length - 4) + "5000";


console.log("URL", URL)

export const socket = io(URL);