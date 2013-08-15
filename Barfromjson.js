
var margin = {top: 35, right: 200, bottom: 20, left: 80},
    width = 960 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

var x = d3.scale.linear()
    .range([0,width]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
  
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg_legend = d3.select("body").append("svg")
    .attr("width", width+margin.left)
    .attr("height", 200)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var leg_grp=svg_legend.append("g");
// 	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var data; // a global
var coldomain=[];
var firstword;
i=0;
var ydomain=[];
var pages=[];

d3.json("hoteltopkwbyurl.json", function(error, json) {
	if (error) return console.warn(error)
		data=json

	console.log('data',data);

	for (word in data.data) 
		ydomain.push(word);

	var y = d3.scale.ordinal()
		.domain(d3.range(ydomain.length))
		.rangeRoundBands([2, height],0.08);

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left") 
		.tickValues(ydomain);
		
	for (word in data.data) 
		if (i===0);
			firstword = word;

	for (key in data.data[firstword])
		{
		if (key !='total')
			coldomain.push(key);
		};

	var color = d3.scale.category20()
		.domain(coldomain);
// 		.range(["#aad", "#556"]);	

	for (word in data.data) 
		{
		y0=0;
		legend={};
		total=0;
		wordobj=data.data[word];
				
		legend=color.domain().map(function(name) {return {i:i, name: name, y0: y0, y1: y0 += +wordobj[name]['count']};});				
		total=data.data[word]['total'];
		var pagesary=function(word,legend,total) {return {word:word, legend:legend, total:total};}
		pages.push(pagesary(word,legend,total));
		++i;
		};
	
	i=0;
	
		  			
	pages.sort(function(a, b) {return b.total-a.total; }); 

	totalsarray=[]; 
	
 	for (word in pages) 
 		{
 		totalsarray.push(parseInt(pages[word]['total']));
 		};
 		
 	console.log('totals',totalsarray,d3.max(totalsarray))
 	 	 	
	x.domain([0,d3.max(totalsarray)]);
	 	 
	svg.append("g") //"g" is DOM shorthand for a "group" object, which is a heuristic that lets you add things to everything in that group later
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")") //this is responsible for moving axis from top (svg default) to bottom		
		.call(xAxis)
		.append("text") 
		.attr("x", width+margin.left)
		.attr("dy", ".71em")
		.style("text-anchor", "end")
		.style("font-size", "16px") 
		.attr("transform", "translate(40,0), rotate(0)")
		.text("Word Counts")
		; 
 
	svg.append("g") 
		.attr("class", "y axis") 
		.call(yAxis)
		.append("text") 
		.attr("y", -17)
		.attr("dy", ".71em")
		.style("text-anchor", "middle")
		.style("font-size", "16px") 
		.attr("transform", "translate(5,0), rotate(0)")
		.text("Keywords")
		;
	
	var txtline="";
	
	svg.selectAll("text")
// 		.style("fill", 'lightsteelblue')
		.on("click",function(d) { 
				wordObj=data.data[d]
				txtline='<br><b>Keyword:</b>'+d+'</br>';
	// 			console.log('txtline',txtline);
				for (urlObj in wordObj)
				{
	// 				console.log('urlObj',urlObj);
					txtline=txtline.concat('<br><b>URL: </b>',urlObj,'</br>');
					txtline=txtline+'<br><b>Comments</b></br>';
	// 				console.log('txtline',txtline);
				
	// 				console.log('sent',wordObj[urlObj]['sent']);
					sentObj=wordObj[urlObj]['sent']
					for (sentObj2 in wordObj[urlObj]['sent'])
					{
	// 					console.log('sentObj',sentObj);
						txtline=txtline.concat('<br>',sentObj[sentObj2],'</br>');
					}
				}
				console.log('doing textupdate');
				
				var container=document.getElementById("feedbacktext");
				container.innerHTML='';
				container.innerHTML=txtline;
				
			}
			);

	console.log('txtline',txtline);
		
	var word = svg.selectAll(".word")
	  .data(pages) 
	.enter().append("g")
	  .attr("class", "g");
							
	word.selectAll("rect")
	  .data(function(pages) {return pages.legend; })
	.enter().append("rect")
	  .attr("height", y.rangeBand())
	  .attr("x", 
	   function(d,i) { 
	  	return x(d.y0)
	  	;})
	  .attr("y", function(d) { return y(d.i); }) 
	  .attr("width", function(d) { return x(d.y1)-x(d.y0);})
	  .style("fill", function(d) { return color(d.name); });

// legend section
	
	var leg_groups=leg_grp.selectAll('g')
		.data(coldomain)
		.enter()
		.append('g')
		.attr("transform", function(d, i) { return "translate(" + (i)*((width-margin.left)/coldomain.length)+",0)";});
	
	leg_groups.append('rect')
    .attr("height", 15)
    .attr("x",45)
//     .attr("x", function(d, i) { return (i+1)*((width-margin.left)/coldomain.length); })
    .attr("width", 15)
    .style("fill", color);	  

	leg_groups.append('text')
		.text(function(d){return d})
		.style("fill", 'black')
		.attr("y", 60)
		.attr("x", 0)
		.attr("text-anchor", "end")
		.style("font-size", "12px") 
		.attr("transform", function(d, i) { return "translate(0,0) rotate(-65," + 0+"," + 0+") "; })

	svg.append("text")
		.attr("x", (width / 4))             
		.attr("y", 0 - (margin.top / 2))
		.attr("text-anchor", "left")  
		.style("font-size", "14px") 
		.text(data['charttitle']);

	svg.append("text")
		.attr("x", (width / 4))             
		.attr("y", 0 - (margin.top / 7))
		.attr("text-anchor", "left")  
		.style("font-size", "10px") 
		.text(data['chartnote']);
	  
});
