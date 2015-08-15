// SYNTAX TEST "cfml.sublime-syntax"
<cfscript>
param name = "test" default = "#now()#";
// <- embedding.cfml source.cfml.script meta.tag.script.cfml entity.name.tag.script.cfml
//    ^ embedding.cfml source.cfml.script meta.tag.script.cfml entity.other.attribute-name.cfml
//            ^ embedding.cfml source.cfml.script meta.tag.script.cfml string.quoted.double.cfml
param name = "test" default = (now() * then);
// <- embedding.cfml source.cfml.script meta.tag.script.cfml entity.name.tag.script.cfml
//    ^ embedding.cfml source.cfml.script meta.tag.script.cfml entity.other.attribute-name.cfml
//                             ^ embedding.cfml source.cfml.script meta.tag.script.cfml support.function.cfml
//                                     ^ embedding.cfml source.cfml.script meta.tag.script.cfml variable.other.cfml
param name = "test" default = now() then;
// <- embedding.cfml source.cfml.script meta.tag.script.cfml entity.name.tag.script.cfml
//    ^ embedding.cfml source.cfml.script meta.tag.script.cfml entity.other.attribute-name.cfml
//                            ^ embedding.cfml source.cfml.script meta.tag.script.cfml support.function.cfml
//                                  ^ embedding.cfml source.cfml.script meta.tag.script.cfml entity.other.attribute-name.cfml
param name = "test"
default = now() then;
// <- embedding.cfml source.cfml.script meta.tag.script.cfml entity.other.attribute-name.cfml
//        ^ embedding.cfml source.cfml.script meta.tag.script.cfml support.function.cfml
//              ^ embedding.cfml source.cfml.script meta.tag.script.cfml entity.other.attribute-name.cfml

transaction {
// <- embedding.cfml source.cfml.script meta.tag.script.cfml entity.name.tag.script.cfml
}

lock timeout="30"{
//               ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.brace.curly.cfml - meta.tag.script.cfml
}
</cfscript>