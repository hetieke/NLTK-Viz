var httpd = require("http").createServer(handler);
var io=require('/Users/mgoold/Virtualenvs/node_modules/socket.io/lib/socket.io').listen(httpd);
var fs = require('fs');
var url = require("url");
var path = require("path");
var port = process.argv[2] || 8080;
var spawn = require('child_process').spawn;

httpd.listen(parseInt(port, 10));	

function handler (request, response) {

  var uri = url.parse(request.url).pathname, 	
  filename = path.join(process.cwd(), uri);  	 
  																						
  console.log(uri);
  
  path.exists(filename, function(exists) {	
    if(!exists) {
      response.writeHead(404, {"Content-Type": "text/plain"});
      response.write("404 Not Found\n");
      response.end();
      return;	//these returns get you out of the function I think
    }

    if (fs.statSync(filename).isDirectory()) filename += '/index.html';  

	fs.readFile(filename, "binary", function(err, file) {		
	  if(err) {        
		response.writeHead(500, {"Content-Type": "text/plain"});
		response.write(err + "\n");
		response.end();
		return;
	  }

      response.writeHead(200);
      response.write(file, "binary");  //otherwise here's where the file gets finally served
      response.end();
    }); //fs.readFile
    
  }); //path.exists
  
}			

io.sockets.on('connection',function(socket) {
	socket.on('btn_api_call', function(argvlist) {
		console.log('server says trying to emit callback');
		socket.emit('serverMessage','client says trying to emit callback');
		var kw_list="'error','problem','suck','issue','broken','wont','dont','cant','hate'"
		var title_text='title_text'
		var start_date='2013-08-14'
		var end_date='2013-08-16'
		var min='10'
		var subdomain='hotel'
		var notsubdomain='mobile'
		var pythonarrays=['-i386','/Users/mgoold/Virtualenvs/venv-p274/bin/python2.7','/Users/mgoold/Documents/NLTKProject/newpythonolabparsing9.3.13.py']
		var finalargs=pythonarrays.concat(argvlist);
		console.log(finalargs);
		var child= spawn('arch',finalargs)
// 		var child= spawn('arch',['-i386','/Users/mgoold/Virtualenvs/venv-p274/bin/python2.7','/Users/mgoold/Documents/NLTKProject/newpythonolabparsing9.1.13.py',kw_list,title_text,min,start_date,end_date,subdomain,notsubdomain])

		child.on('exit',function(code,signal) {
			if (code){
				console.log('child process terminated with code' + code);
				socket.emit('serverMessage','completed child process');
			} 
			else if (signal) {
				console.log('child process terminated because of signal' + signal);
			}
			else { console.log('some other  result')
				socket.emit('serverMessage','trying to reload');
				socket.emit('jsonSuccess');
			}
		
		});
	});
});

console.log("Static file server running at\n  => http://localhost:" + port + "/\nCTRL + C to shutdown");
