// SYNTAX TEST "cfml.sublime-syntax"
component extends = "root.model.text"
// random comment
persistent = true {
// <- embedding.cfml source.cfml.script meta.class.cfml entity.other.attribute-name.cfml
//           ^ embedding.cfml source.cfml.script meta.class.cfml string.unquoted.cfml
  property test;
//         ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.unquoted.cfml
  property test test;
//         ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml storage.type.cfml
//              ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.unquoted.cfml
  property test test test;
//         ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml storage.type.cfml
//              ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.unquoted.cfml
//                   ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml entity.other.attribute-name.cfml
  property name="test" required=true;
//         ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml entity.other.attribute-name.cfml
//               ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.quoted.double.cfml
//                              ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.unquoted.cfml
//                                  ^ embedding.cfml source.cfml.script meta.group.braces.curly punctuation.terminator.statement.cfml
  property
    name = "test"
    required=true;
//  ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml entity.other.attribute-name.cfml
//           ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.unquoted.cfml
  property test
//         ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.unquoted.cfml
default="string";
// <- embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml entity.other.attribute-name.cfml
//       ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml string.quoted.double.cfml

  function foo() {
    var result;

   	toString( testVar, "utf-8" );
//  ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly support.function.cfml
//          ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly meta.support.function-call.arguments.cfml meta.support.function-call.arguments.begin.cfml
//                             ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly meta.support.function-call.arguments.cfml meta.support.function-call.arguments.end.cfml
    if ( true ) http url="www.google.com" result="result";
//              ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly meta.tag.script.cfml entity.name.tag.script.cfml
//                   ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.tag.script.cfml entity.other.attribute-name.cfml
    return result = foo;
//         ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly variable.other.cfml
//                  ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly variable.other.cfml
    return result == test ? 'one' : 2;
//         ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly variable.other.cfml
//                   ^ embedding.cfml source.cfml.script meta.group.braces.curly meta.group.braces.curly variable.other.cfml
  }

}