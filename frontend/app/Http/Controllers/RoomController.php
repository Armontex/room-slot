<?php

namespace App\Http\Controllers;

use App\Support\FastApiClient;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\View\View;

final class RoomController extends Controller
{
    public function index(FastApiClient $api): View
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

    public function show(string $roomId, FastApiClient $api): View
    {
        $token = session('access_token');

        try {
            $roomResponse = $api->get("/rooms/{$roomId}", token: $token);
            $slotsResponse = $api->get("/rooms/{$roomId}/slots", token: $token);
        } catch (ConnectionException) {
            return view('rooms.show', [
                'room' => null,
                'slotsSchedule' => null,
                'error' => 'Room service is unavailable',
            ]);
        }

        if ($roomResponse->failed()) {
            return view('rooms.show', [
                'room' => null,
                'slotsSchedule' => null,
                'error' => 'Failed to load room',
            ]);
        }

        if ($slotsResponse->failed()) {
            return view('rooms.show', [
                'room' => $roomResponse->json(),
                'slotsSchedule' => null,
                'error' => 'Failed to load room slots',
            ]);
        }

        return view('rooms.show', [
            'room' => $roomResponse->json(),
            'slotsSchedule' => $slotsResponse->json(),
            'error' => null,
        ]);
    }
}
