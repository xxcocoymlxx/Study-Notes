//select worksheet

int main (int argc , char ** argv){
 	if ( argc != 3){
 		fprintf(stderr,"Usage :\n\tnetcat IP PORT");
 		return 1;
 	}

 	char buf[MAXSIZE];
 	//create the socket
 	int soc = socket(AF_INET,SOCK_STREAM,0);
 	if (soc < 0){
 		perror("socket");
 		exit(1);
 	}


 	//set up the sockaddr_in struct for connecting
 	struct sockaddr_in peer;
 	peer.sin_family = AF_INET;
 	peer.sin_port = htons(strtol(argv[2],NULL,10));
 	//for security reason
 	memset(&peer.sin_zero,0,8);


 	if (inet_pton(AF_INET,argv[1],&peer.sin_addr)<0){//convert the ip address from string to .. so we can store it in the sockaddr_in sturcture
 		perror("inet_pton");
 		close(soc);
 		exit(1);
 	}

 	//connect the socket
 	if (connect(soc,(struct sockaddr*)peer,sizeof(peer))<0){
 		perror("connect");
 		close(soc);
 		exit(1);
 	}


 	//anything else to do before the following infinite loop
 	fd_set fdset, fdall;
 	FD_ZERO(&fdall);

 	FD_SET(soc,&fdall);
 	FD_SET(fileno(stdin),&fdall);

 	int byte_read = 0;


 	while (1){
 		fdset = fdall;
 		//use an fd_set and select to wait for keyboard or server input
 		//或者可以写成
 		//FD_SET(soc,&fdset);
 		//FD_SET(fileno(stdin),&fdset);
 		if (select(soc+1,&fdset,NULL,NULL,NULL)<0){
 			perror("socket");
 			exit(1);
 		}

 		// If there is data from stdin , send to server
 		if (FD_ISSET(fileno(stdin),&fdset)){
 			byte_read = read(fileno(stdin),&buf, MAXSIZE);
 			//error checking here
 			write(soc,&buf,byte_read);
 		}


 		//If there is data from the server , print to stdout
 		if (FD_ISSET(soc,&fdset)){
 			byte_read = read(soc,&buf, MAXSIZE);
 			//error checking here

 			//if the client is disconnected, byte_read is gonna be 0
 			if (byte_read == 0){
 				perror("client is disconnected");
 				exit(1);
 			}
 			write(fileno(stdout),&buf,byte_read);
 		}

 	}
 	return 0;
 }





