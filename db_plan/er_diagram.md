<!-- ```mermaid
---
title: Overview of Relationships
---
erDiagram
    ENTRY |{--|| FOCUS_AREA : contains 
    ENTRY |{--|| PROJECTS : contains
    ENTRY |{--|{ ACTIVITY_TYPE : contains
    ENTRY ||--|{ TIME_ELAPSED : contains

    FOCUS_AREA || -- |{ PROJECTS : connects_to

``` -->

[comment]:  An ENTRY can have only one FOCUSE_AREA, while a FOCUS_AREA can connect to many ENTRYs
[comment]:  An ENTRY can have connect to many TIME_ELAPSED, while a TIME_ELAPSED can connect to only one ENTRY


