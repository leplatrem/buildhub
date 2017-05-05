module Types
    exposing
        ( Build
        , BuildRecord
        , Download
        , Model
        , Msg(..)
        , Source
        , SystemAddon
        , Target
        )

import Kinto


type alias Model =
    { builds : List BuildRecord
    , treeList : List String
    , productList : List String
    , versionList : List String
    , platformList : List String
    , channelList : List String
    , localeList : List String
    , loading : Bool
    }


type alias BuildRecord =
    { id : String
    , last_modified : Int
    , build : Build
    , download : Download
    , source : Source
    , systemAddons : Maybe (List SystemAddon)
    , target : Target
    }


type alias Build =
    { date : String
    , id : String
    , type_ : String
    }


type alias Download =
    { mimetype : Maybe String
    , size : Maybe Int
    , url : String
    }


type alias Source =
    { product : String
    , tree : String
    , revision : Maybe String
    }


type alias SystemAddon =
    { id : String
    , builtinVersion : Maybe String
    , updatedVersion : Maybe String
    }


type alias Target =
    { version : Maybe String
    , platform : String
    , channel : Maybe String
    , locale : String
    }


type Msg
    = BuildRecordsFetched (Result Kinto.Error (List BuildRecord))
