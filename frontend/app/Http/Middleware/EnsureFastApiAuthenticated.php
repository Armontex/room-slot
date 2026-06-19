<?php

namespace App\Http\Middleware;

use App\Support\FastApiClient;
use Closure;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class EnsureFastApiAuthenticated
{
    public function __construct(
        private readonly FastApiClient $api,
    ) {
    }

    public function handle(Request $request, Closure $next): Response
    {
        $token = session('access_token');

        if ($token === null) {
            return redirect('/login');
        }

        try {
            $response = $this->api->get('/auth/me', token: $token);
        } catch (ConnectionException) {
            return redirect('/login')
                ->withErrors(['email' => 'Auth service is unavailable']);
        }

        if ($response->failed()) {
            session()->forget('access_token');

            return redirect('/login');
        }

        $request->attributes->set('user', $response->json());

        return $next($request);
    }
}
