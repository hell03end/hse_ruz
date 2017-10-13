# RUZ API description
Full list of RUZ HSE API methods with short description.

### Endpoints
Currently there are 2 versions of RUZ API and not all endpoints support `v2`.

Possible endpoints (not all of them works with `v2`):
* [x] [`personLessons`](#PersonLessons) - return classes schedule
* [ ] [`groups`](#Groups) - return list of groups
* [ ] [`staffOfGroup`](#StaffOfGroup) - return list of students in group
* [ ] [`streams`](#Streams) - return list of study streams
* [ ] [`staffOfStreams`](#StaffOfStreams) - return list of the groups on study stream
* [ ] [`lecturers`](#Lecturers) - return list of teachers
* [ ] [`auditoriums`](#Auditoriums) - return list of auditoriums
* [ ] [`typeOfAuditoriums`](#TypeOfAuditoriums) - return list of auditoriums' types
* [ ] [`kindOfWorks`](#KindOfWorks) - return list of classes' types
* [ ] [`buildings`](#Buildings) - return list of buildings
* [ ] [`faculties`](#Faculties) - return list of learning programs (faculties)
* [ ] [`chairs`](#Chairs) - return list of departments
* [ ] [`subGroups`](#SubGroups) - return list of subgroups

#### PersonLessons
Input params:
* `fromDate` - start of the period YYYY.MM.DD, required
* `toDate` - end of the period YYYY.MM.DD, required
* `receiverType` - type of the schedule (1/2/3 for teacher/auditorium/student)
* `groupOid` - ID of group
* `lecturerOid` - ID of teacher
* `auditoriumOid` - ID of auditorium
* `studentOid` - ID of student
* `email` - e-mail on hse.ru (edu.hse.ru for students)
* `UNS`

*One of the followed required: `lecturerOid`, `groupOid`, `auditoriumOid`, `studentOid`, `email`*

<!--
Response:
```json
[{
   "auditorium":"XXX",
   "auditoriumOid":NNNN,
   "beginLesson":"XX:XX",
   "building":"XXXXXXXXX ул., д. XX",
   "date":"NNNN.NN.NN",
   "dateOfNest":"\/Date(NNNNNNNNNNNNN+NN00)\/",
   "dayOfWeek":N,
   "dayOfWeekString":"Пн",
   "discipline":"XXXXXXXXX (рус)",
   "endLesson":"NN:NN",
   "group":null,
   "groupOid":0,
   "kindOfWork":"Лекция",
   "lecturer":"XXXXXXXXX X.X.",
   "lecturerOid":XXXXXX,
   "stream":"XXXNNN;XXXNNN;XXXNNN#XXXXXXXXXX",
   "streamOid":XXXXXXX,
   "subGroup":null,
   "subGroupOid":0
}]
```
 -->

#### Groups
Input params:
* `facultyOid` - course ID
* `findText` - text to find

<!--
Response:
```json
[{
   "chairOid":0,
   "course":2,
   "faculty":"T 00.00.00 YYYY form XXXXXXXXXXXXXX", // where T means type
   "facultyOid":0000,
   "formOfEducation": "str",
   "groupOid":0000,
   "number":"01",
   "speciality":""
}]
```
-->


#### StaffOfGroup
Input params:
* `groupOid` - group' ID, required
* `findText` - text to find

<!--
Response:
```json
[{
   "fio":"Name Surname LastName",
   "shortFIO":"Surname N.L.",
   "studentOid":00000
}]
```
-->

#### Streams
Input params:
* `findText` - text to find

<!--
Response:
```json
[{
   "abbr":"БИИ100,БИИ101",
   "course":"0",
   "faculty":"Б 00.00.00 2010 очная XXXXXXXXXXXXXX",
   "facultyOid":0000,
   "formOfEducation":"очная форма обучения",
   "name":"БИИ100,БИИ101",
   "streamOid":0000,
   "yearOfEducation":2010
}]
```
-->

#### StaffOfStreams
Input params:
* `streamOid` - group' ID, required

<!--
Response:
```json
[{
   "GroupNumber":"БИИ150",
   "GroupOid":0000,
   "SubgroupName":"БИИ150",
   "SubgroupOid":00000
}]
```
-->

#### Lecturers
Input params:
* `chairOid` - ID of department
* `findText` - text to find

<!--
Response:
```json
[{
   "chair":"!Не определена",
   "chairOid":1,
   "fio":"!Вакансия",
   "lecturerOid":1,
   "shortFIO":"!Вакансия "
}]
```
-->

#### Auditoriums
Input params:
* `buildingOid` - ID of building
* `findText` - text to find

<!--
Response:
```json
[{
   "auditoriumOid":000,
   "building":"ул. XXX NN",
   "buildingOid":00,
   "number":"001",
   "typeOfAuditorium":"Компьютерный класс"
}]
```
-->

#### TypeOfAuditoriums

<!--
Response:
```json
[{
   "abbr":"ЯА",
   "code":"",
   "name":"Языковая",
   "typeOfAuditoriumOid":0
}]
```
-->

#### KindOfWorks

<!--
Response:
```json
[{
   "abbr":"Контрольная работа",
   "code":"Контрольная работа",
   "complexity":0,
   "kindOfWorkOid":866,
   "name":"Контрольная работа",
   "unit":""
}]
```
-->

#### Buildings
Input params:
- `findText` - text to find

<!--
Response:
```json
[{
   "abbr":"XXXXXXXXXX",
   "address":"Москва, XXXXXXX, NN",
   "buildingOid":XX,
   "name":"XXXXXXXXXXX"
}]
```
-->

#### Faculties
Input params:
* `findText` - text to find

<!--
Response:
```json
[{
   "abbr":"XXX NNN",
   "code":"Б0X0X0XNNNN",
   "facultyOid":0000,
   "institute":"Факультет XXXXXXXXXX",
   "name":"Б 00.00.00 NNNN очная XXXXXXXXX"
}]
```
-->

#### Chairs
Input params:
* `facultyOid` - ID of course (learning program)
* `findText` - text to find

<!--
Response:
```json
[{
   "abbr":"XXXXXXXXXXXX",
   "chairOid":NNN,
   "code":"00",
   "faculty":"",
   "facultyOid":0,
   "name":"XXXXXX XXXXXX XXXXXX"
}]
```
-->

#### SubGroups
Input params:
* `findText` - text to find

<!--
Response:
```json
[{
   "abbr":"XXXNNN_1",
   "group":"XXXNNN",
   "groupOid":0000,
   "name":"XXXNNN_1#",
   "subGroupOid":00000
}]
```
-->
