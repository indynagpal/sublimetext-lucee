<!--- SYNTAX TEST "cfml.sublime-syntax" --->
<div>
 <!--- <- embedding.cfml text.html.cfml meta.tag entity.name.tag --->
<cfset testArray = []>
 <!--- <- embedding.cfml entity.name.tag --->
<cfset arrayAppend(testArray, 1)>
<!---  ^ embedding.cfml meta.tag source.cfml.script meta.support.function-call.cfml support.function.cfml --->
<!---             ^ embedding.cfml meta.tag source.cfml.script meta.support.function-call.arguments.cfml punctuation.definition.arguments.begin.cfml --->
</div>
<cfoutput>
<!---     ^ embedding.cfml text.html.cfml meta.scope.cfoutput.cfml text.html.cfml --->
#now()#
<!--- <- embedding.cfml text.html.cfml meta.scope.cfoutput.cfml text.html.cfml constant.character.hash.cfml.start --->
  <!--- <- embedding.cfml text.html.cfml meta.scope.cfoutput.cfml text.html.cfml source.cfml.script support.function.cfml --->
</cfoutput>
<cfscript>
foo = 'hello world';
<!--- <- embedding.cfml text.html.cfml source.cfml.script variable.other.cfml --->
<!---  ^ embedding.cfml text.html.cfml source.cfml.script string.quoted.single.cfml --->
<!---              ^ embedding.cfml text.html.cfml source.cfml.script punctuation.terminator.statement.cfml --->

arrayAppend(foo, 10);
<!--- <- embedding.cfml text.html.cfml source.cfml.script meta.support.function-call.cfml support.function.cfml --->
<!---      ^ embedding.cfml text.html.cfml source.cfml.script meta.support.function-call.cfml meta.support.function-call.arguments.cfml punctuation.definition.arguments.begin.cfml --->
<!---              ^ embedding.cfml text.html.cfml source.cfml.script meta.support.function-call.cfml meta.support.function-call.arguments.cfml punctuation.definition.arguments.end.cfml --->
myArray.append(10);
<!---   ^ embedding.cfml text.html.cfml source.cfml.script meta.support.function-call.member.cfml support.function.member.cfml --->
<!---         ^ embedding.cfml text.html.cfml source.cfml.script meta.support.function-call.member.cfml meta.support.function-call.member.arguments.cfml punctuation.definition.arguments.begin.cfml --->
myFunc();
<!--- <- embedding.cfml text.html.cfml source.cfml.script meta.function-call.cfml variable.function.cfml --->
<!--- ^ embedding.cfml text.html.cfml source.cfml.script meta.function-call.cfml meta.function-call.arguments.cfml punctuation.definition.arguments.begin.cfml --->
myFunc(10);
<!--- <- embedding.cfml text.html.cfml source.cfml.script meta.function-call.cfml variable.function.cfml --->
<!--- ^ embedding.cfml text.html.cfml source.cfml.script meta.function-call.cfml meta.function-call.arguments.cfml punctuation.definition.arguments.begin.cfml --->
myObj.addVal(10);
<!--- <- embedding.cfml text.html.cfml source.cfml.script variable.other.object.cfml --->
<!--- ^ embedding.cfml text.html.cfml source.cfml.script meta.function-call.method.cfml --->
<!---       ^ embedding.cfml text.html.cfml source.cfml.script meta.function-call.method.cfml meta.function-call.method.arguments.cfml punctuation.definition.arguments.begin.cfml --->
myFunc().addVal(10);
<!--- <- embedding.cfml text.html.cfml source.cfml.script meta.function-call.cfml variable.function.cfml --->
<!--- ^ embedding.cfml text.html.cfml source.cfml.script meta.function-call.cfml meta.function-call.arguments.cfml punctuation.definition.arguments.begin.cfml --->
<!---    ^ embedding.cfml text.html.cfml source.cfml.script meta.function-call.method.cfml --->
<!---          ^ embedding.cfml text.html.cfml source.cfml.script meta.function-call.method.cfml meta.function-call.method.arguments.cfml punctuation.definition.arguments.begin.cfml --->
</cfscript>