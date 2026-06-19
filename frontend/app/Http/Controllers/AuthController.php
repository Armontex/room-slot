<?php

namespace App\Http\Controllers;

use App\Support\FastApiClient;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

final class AuthController extends Controller
{
    public function showLogin(): View
    {
        return view('auth.login');
    }

    public function login(Request $request, FastApiClient $api): RedirectResponse
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

        $token = $response->json('access_token');

        if ($token === null) {
            return back()
                ->withErrors(['email' => 'Invalid auth response'])
                ->onlyInput('email');
        }

        $request->session()->regenerate();

        session([
            'access_token' => $token,
        ]);

        return redirect('/rooms');
    }

    public function showRegister(): View
    {
        return view('auth.register');
    }

    public function register(Request $request, FastApiClient $api): RedirectResponse
    {
        $payload = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ]);

        $response = $api->post('/auth/register', $payload);

        if ($response->failed()) {
            return back()
                ->withErrors(['email' => 'Registration failed'])
                ->onlyInput('email');
        }

        return redirect('/login');
    }

    public function logout(Request $request): RedirectResponse
    {
        $request->session()->forget('access_token');
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/login');
    }
}
