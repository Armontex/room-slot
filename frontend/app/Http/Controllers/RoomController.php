<?php

namespace App\Http\Controllers;

use App\Support\FastApiClient;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Request;
use Illuminate\View\View;

final class RoomController extends Controller
{
    public function index(Request $request, FastApiClient $api): View
    {
        $token = session('access_token');

        try {
            $response = $api->get('/rooms', [
                'offset' => 0,
                'limit' => 10,
            ], token: $token);
        } catch (ConnectionException) {
            return view('rooms.index', [
                'rooms' => [],
                'total' => 0,
                'limit' => 10,
                'offset' => 0,
                'error' => 'Room service is unavailable',
            ]);
        }

        if ($response->failed()) {
            return view('rooms.index', [
                'rooms' => [],
                'total' => 0,
                'limit' => 10,
                'offset' => 0,
                'error' => 'Failed to load rooms',
            ]);
        }

        return view('rooms.index', [
            'rooms' => $response->json('items') ?? [],
            'total' => $response->json('total') ?? 0,
            'limit' => $response->json('limit') ?? 10,
            'offset' => $response->json('offset') ?? 0,
            'error' => null,
        ]);
    }
}
