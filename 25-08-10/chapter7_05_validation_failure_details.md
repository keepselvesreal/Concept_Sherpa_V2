"""
생성 시간: 2025-08-10 22:28:30 KST
핵심 내용: 데이터 검증 실패 세부 정보 (7.5절) - 검증 오류의 상세 정보 획득
상세 내용:
    - 검증 실패의 이진성 극복 (739-743행): 단순한 true/false를 넘어 상세 정보 제공
    - 검증 오류 세부 정보 (744-754행): 누락 필드, 잘못된 타입 등의 구체적 정보
    - Ajv 라이브러리 사용법 (755-781행): validator 인스턴스를 통한 오류 접근
    - 단일 검증 실패 예제 (782-800행): title 필드 누락 시 오류 배열 구조
    - 인간 친화적 오류 메시지 (801-807행): errorsText 유틸리티 함수 사용
    - 다중 검증 실패 처리 (808-847행): allErrors 옵션을 통한 모든 오류 수집
    - Joe의 선물 (854-893행): JSON Schema cheat sheet 제공
    - 유효한 데이터 예제 (894-913행): cheat sheet 뒷면의 실제 데이터 예시
상태: 활성
주소: chapter7_05_validation_failure_details
참조: 원본 파일 /home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts/Level01_7 Basic data validation.md
"""

# 7.5 Details about data validation failures

7.5 Details about data validation failures
Joe So far, we've treated JSON Schema validation as though it were binary: either a
piece of data is valid or it isn't.
Theo Right...
Joe But, in fact, when a piece of data is not valid, we can get details about the
reason of the invalidity.
Theo Like when a required field is missing, can we get the name of the missing field?
Joe Yes. When a piece of data is not of the expected type, we can get information
about that also.
Theo That sounds very useful!
Joe Indeed. Let me show you how it works. Until now, we used a generic validate
function, but when we deal with validation failures, we need to be more specific.
Theo Why?
Joe Because each data validator library has its own way of exposing the details of
 data validation failure. For instance, in JavaScript Ajv, the errors from the
last data validation are stored as an array inside the validator instance.
Theo Why an array?
Joe Because there could be several failures. But let's start with the case of a single
failure. Imagine we encounter a search book request where the title field is
named myTitle instead of title. Take a look at this example. As you can see,
we first instantiate a validator instance.
Listing7.20 Accessing validation errors in Ajv
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}
}
},
"required": ["title", "fields"]
};
var invalidSearchBooksRequest = {
"myTitle": "habit",
"fields": ["title", "weight", "number_of_pages"]
};
Instantiates a
var ajv = new Ajv(); validator instance
ajv.validate(searchBooksRequestSchema, invalidSearchBooksRequest);
ajv.errors
Displays the
validation errors

=== 페이지 187 ===
7.5 Details about data validation failures 159
Theo And what does the information inside the errors array look like?
Joe Execute the code snippet. You'll see.
When Theo executes the code snippets from listing 7.20, he can hardly believe his eyes. He
looks at the details, finding the results hard to digest.
Listing7.21 Details for a single data validation failure in an array format
[
{
"instancePath": "",
"schemaPath": "#/required",
"keyword": "required",
"params": {
"missingProperty":"title"
},
"message": "must have required property 'title'"
}
]
Theo I find the contents of the errors array a bit hard to understand.
Joe Me too. Fortunately, Ajv provides a errorsText utility function to convert the
errors array in a human readable format. See, for instance, what is returned
when you call errorsText.
Listing7.22 Displaying the errors in human readable format
ajv.errorsText(ajv.errors);
// → "data must have required property 'title'"
Theo Let me see what happens when there are more than one validation failure in
the data.
Joe By default, Ajv catches only one validation error.
TIP By default, Ajv catches only the first validation failure.
Theo I guess that's for performance reasons. Once the validator encounters an
error, it doesn't continue the data parsing.
Joe Probably. Anyway, in order to catch more than one validation failure, you need
to pass the allErrors options to the Ajv constructor. Check out this code.
Listing7.23 Catching multiple validation failures
var searchBooksRequestSchema = {
"type": "object",
"properties": {
"title": {"type": "string"},
"fields": {
"type": "array",
"items": {"type": "string"}

=== 페이지 188 ===
160 CHAPTER 7 Basic data validation
}
},
"required": ["title", "fields"]
};
A request with
three failures
var invalidSearchBooksRequest = {
"myTitle": "habit",
"fields": [1, 2]
}; Instantiates the Ajv constructor
with allErrors: true in order to
catch more than one failure
var ajv = new Ajv({allErrors: true});
ajv.validate(searchBooksRequestSchema,
invalidSearchBooksRequest); Converts the
errors to a human
readable format
ajv.errorsText(ajv.errors);
// → "data must have required property 'title',
// → data/fields/0 must be string,
// → data/fields/1 must be string"
Joe We validate a search request with myTitle instead of title and numbers
instead of strings in the fields array. As you can see in the output of the code
snippet, three errors are returned.
Theo Great! I think I have all that I need in order to add data validation to the
boundaries of my system when Nancy asks me to make the Library Manage-
ment System into a web server.
Joe Would you allow me to give you a small gift as a token of our friendship?
Theo I'd be honored.
Joe takes a small package out of his bag, wrapped in a light-green ribbon. He hands Theo
the package with a solemn gesture.
When Theo undoes the ribbon, he discovers an elegant piece of paper decorated with
pretty little designs. In the center of the paper, Theo manages to read the inscription
"JSON Schema cheat sheet." He smiles while browsing the cheat sheet. It's exactly what he
needs.
Listing7.24 JSON Schema cheat sheet
{ At the root level,
data is an array.
"type": "array",
"items": { Each element of the
array is a map.
"type": "object",
myNumber "properties": {
The properties of
is a number. "myNumber": {"type": "number"},
each field in the map
"myString": {"type": "string"},
myString is
"myEnum": {"enum": ["myVal", "yourVal"]},
a string. myEnum is a
"myBool": {"type": "boolean"}
enumeration
myBool is a }, value with two
boolean. "required": ["myNumber", "myString"], possibilities:
The mandatory fields in the map "myVal" and
are myNumber and myString; "yourVal".
other fields are optional.

=== 페이지 189 ===
Summary 161
"additionalProperties": false
We don't allow fields that
}
are not explicitly mentioned
}
in the schema.
Then, Theo turns the paper over to find that the back is also filled with drawings. In the
center of the paper, he reads the inscription, "An example of valid data."
Listing7.25 An example of valid data
[
{
This map is valid
"myNumber": 42,
because all its
"myString": "Hello",
fields are valid.
"myEnum": "myVal",
"myBool": true
},
{
This map is valid
"myNumber": 54,
because it contains all
"myString": "Happy"
the required fields.
}
]