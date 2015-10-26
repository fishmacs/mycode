package com.mblinn.oo.tinyweb;

public interface Controller {
  public HttpResponse handleRequest(HttpRequest httpRequest);
}
