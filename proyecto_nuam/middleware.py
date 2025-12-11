"""Custom middleware for session control and cache headers."""

from typing import Callable

from django.http import HttpRequest, HttpResponse


class NoCacheMiddleware:
	"""Sets strict no-cache headers so back button can't show stale pages after logout."""

	def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
		self.get_response = get_response

	def __call__(self, request: HttpRequest) -> HttpResponse:
		response = self.get_response(request)

		content_type = response.get('Content-Type', '')
		if 'text/html' in content_type:
			response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
			response['Pragma'] = 'no-cache'
			response['Expires'] = '0'

		return response
