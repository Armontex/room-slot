<?php

namespace App\Http\Controllers;

use App\Support\FastApiClient;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\View\View;

final class MeController extends Controller
{
    public function index(FastApiClient $api): View
    {
        $token = session('access_token');

        try {
            $authResponse = $api->get('/auth/me', token: $token);
            $bookingsResponse = $api->get('/me/bookings', [
                'offset' => 0,
                'limit' => 10,
            ], token: $token);
        } catch (ConnectionException) {
            return view('me.index', [
                'user' => null,
                'bookings' => [],
                'total' => 0,
                'limit' => 10,
                'offset' => 0,
                'error' => 'Profile service is unavailable',
            ]);
        }

        if ($authResponse->failed()) {
            return view('me.index', [
                'user' => null,
                'bookings' => [],
                'total' => 0,
                'limit' => 10,
                'offset' => 0,
                'error' => 'Failed to load profile',
            ]);
        }

        if ($bookingsResponse->failed()) {
            return view('me.index', [
                'user' => $authResponse->json(),
                'bookings' => [],
                'total' => 0,
                'limit' => 10,
                'offset' => 0,
                'error' => 'Failed to load bookings',
            ]);
        }

        return view('me.index', [
            'user' => $authResponse->json(),
            'bookings' => $bookingsResponse->json('items') ?? [],
            'total' => $bookingsResponse->json('total') ?? 0,
            'limit' => $bookingsResponse->json('limit') ?? 10,
            'offset' => $bookingsResponse->json('offset') ?? 0,
            'error' => null,
        ]);
    }
}
