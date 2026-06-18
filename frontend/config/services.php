<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Third Party Services
    |--------------------------------------------------------------------------
    |
    | This file is for storing the credentials for third party services such
    | as Mailgun, Postmark, AWS and more. This file provides the de facto
    | location for this type of information, allowing packages to have
    | a conventional file to locate the various service credentials.
    |
    */

    'fastapi' => [
        'url' => env('FASTAPI_URL', 'http://localhost:8000'),
        'ws_url' => env('FASTAPI_WS_URL', 'ws://localhost:8000'),
    ],

];
