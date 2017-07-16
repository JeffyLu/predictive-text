<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <base href="<%=basePath%>">
    
    <title>My JSP 'index.jsp' starting page</title>
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">    
	<meta http-equiv="words" content="word1,word2,word3">
	<meta http-equiv="description" content="This is my page">
	<style type="text/css">
     	#tex{
     			border-top:100px solid white;         /*上边框样式*/
                border-left:400px solid white; 
     		}
     	#word{
     		width:500px;
     		height:200px;
     	}
     </style>
	<script type="text/javascript" src="js/jquery-3.2.0.min.js"></script>
	<script type="text/javascript">
	var num = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];
function getMes(){
	var word=$("#word").val();
	var last_alpha = word[word.length -1];
	if (num.indexOf(last_alpha) != -1){
		word = word.substring(0, word.lastIndexOf(' ')) + $("#word" + last_alpha).html().substring(2);
		$("#word").val(word);
	}
	else{
		var formData={
			word:word
		}
		var remindURL="remindAction!remind";
		jQuery.post(remindURL,formData,function(jsonData){
		    	clearContent();
		    	setContent(jsonData);
			},"json");
	
	}
}       

function setContent(contents){
	//清空之前的数据
	clearContent();
	//设置位置
	//首先获得关联数据的长度，以此来确定生成多少个<tr></tr>
	var size = contents.length;
	//设置内容
	for(var i =0;i < size;i++){
		var nextNode = contents[i];//代表json数据的第i个元素
		var tr = document.createElement("tr");
		var td = document.createElement("td");
		td.setAttribute("id", "word"+(i+1));
		td.setAttribute("borde","0");
		td.setAttribute("gbcolor","#FFFAFA");
		//为td绑定两个样式（鼠标进入和鼠标移出时事件）
		td.onmouseover = function(){
			this.className = 'mouseOver';
		};
		td.onmouseout = function(){
			this.className = 'mouseOut';
		};
		td.onclick = function(){
			//这个方法实现的是，当用鼠标点击一个关联数据时，关联数据自动填充到输入框中。
		};
		td.onmousedown = function(){
        	//当鼠标点击一个关联数据时，自动在输入框添加数据
        	document.getElementById("word").value =this.innerText;
       };
		//创建一个文本节点
		var text = document.createTextNode(nextNode);
		td.appendChild(text);
		tr.appendChild(td);
		document.getElementById("content_table_body").appendChild(tr);
	}
}
function clearContent(){
   	var tb = document.getElementById("tab");
	var rowNum=tb.rows.length;
	for (i=rowNum-1;i>=0;i--)
    {
  	   tb.deleteRow(i);
    }
}
</script>
</head>
   <body>
    <div id="tex">
    	<h3>英文写作助手</h3>  
    	<textarea id="word" onkeyup="getMes()" ></textarea>
    	<div id="ajaxMes">
    		<table id="tab">
    			<tbody id="content_table_body">
    			</tbody>
    		</table>
    	</div>
    </div>
  </body>
</html>
