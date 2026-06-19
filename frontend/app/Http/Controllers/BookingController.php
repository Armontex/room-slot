<?php

namespace App\Http\Controllers;

use App\Support\FastApiClient;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

final class BookingController extends Controller
{
    public function store(Request $request, FastApiClient $api): RedirectResponse
    {
        $payload = $request->validate([
            'room_id' => ['required', 'uuid'],
            'date' => ['required', 'date'],
            'start_time' => ['required', 'date_format:H:i:s'],
        ]);

        $token = session('access_token');

        try {
            $response = $api->post('/bookings', $payload, token: $token);
        } catch (ConnectionException) {
            return back()
                ->withErrors(['booking' => 'Booking service is unavailable']);
        }

        if ($response->failed()) {
            return back()
                ->withErrors(['booking' => 'Failed to create booking']);
        }

        return redirect()
            ->route('rooms.show', ['roomId' => $payload['room_id']]);
    }

}
