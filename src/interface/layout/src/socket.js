import socketIOClient from 'socket.io-client';

const socket = socketIOClient("/user");
export default socket;