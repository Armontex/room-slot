<?php

namespace App\Http\Controllers;

use App\Support\FastApiClient;
use Illuminate\Http\Request;

final class AuthController extends Controller
{
    public function showLogin()
    {
        return view('auth.login');
    }

    public function login(Request $request, FastApiClient $api)
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required', 'string'],
        ]);

        $response = $api->post('/auth/login', $credentials);

        if ($response->failed()) {
            return back()
                ->withErrors(['email' => 'Invalid credentials'])
                ->onlyInput('email');
        }

        session([
            'access_token' => $response->json('access_token'),
        ]);

        return redirect('/rooms');
    }
}
