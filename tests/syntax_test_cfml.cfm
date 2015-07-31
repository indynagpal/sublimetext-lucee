<!--- SYNTAX TEST "cfml.sublime-syntax" --->
<div>
 <!--- <- embedding.cfml text.html.cfml meta.tag entity.name.tag --->
<cfset testArray = []>
 <!--- <- embedding.cfml entity.name.tag --->
<cfset arrayAppend(testArray, 1)>
<!---   ^ embedding.cfml meta.tag source.cfml.script support.function.cfml --->
<!---             ^ embedding.cfml meta.tag source.cfml.script meta.brace.round.cfml --->
</div>
<cfoutput>
<!---     ^ embedding.cfml text.html.cfml meta.scope.cfoutput.cfml text.html.cfml --->
#now()#
<!--- <- embedding.cfml text.html.cfml meta.scope.cfoutput.cfml text.html.cfml constant.character.hash.cfml.start --->
  <!--- <- embedding.cfml text.html.cfml meta.scope.cfoutput.cfml text.html.cfml source.cfml.script support.function.cfml --->
</cfoutput>
<cfscript>
foo = 'hello world';/*
<!--- <- embedding.cfml text.html.cfml source.cfml.script variable.other.cfml
<!---   ^ embedding.cfml text.html.cfml source.cfml.script string.quoted.single.cfml
<!---              ^ embedding.cfml text.html.cfml source.cfml.script punctuation.terminator.statement.cfml

*/
</cfscript>