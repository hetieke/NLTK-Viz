var commentapp={
	init:function(){
		var commentapp=this;
		commentapp.socket=io.connect('http://localhost:8080');	
		commentapp.socket.on('serverMessage', function(content){
			console.log(content);
		});	
		commentapp.socket.on('jsonSuccess', function(){
			console.log('client trying to trigger reload');
			drawOlabsvg.redrawAll();
		});			
		
	
		commentapp.btn_api=$('#btn_api'); 		
		commentapp.btn_api.click(this.get_comment_data);
		
					
	},
	get_comment_data: function(){
		var commentapp=this;
		console.log('trying to connect');
		commentapp.socket=io.connect('http://localhost:8080');	
		
		console.log('getting olab script arguments');
		var arglist=new Array();

// script, DESIRE, test_title, min, start_date, end_date,subdomain,notsubdomain= argv

		arglist[0]=$('#keywordlist').val(); 
		arglist[1]='Trending Keywords';
		arglist[2]=$('#minwordcount').val(); 
		arglist[3]=$('#startdate').val(); 
		arglist[4]=$('#enddate').val(); 		
		arglist[5]=$('#domaininput').val(); 
		arglist[6]=$('#subdomainput').val(); 
											
		commentapp.socket.emit('btn_api_call',arglist);
	}
	
};

$(function() {
  commentapp.init();
});

