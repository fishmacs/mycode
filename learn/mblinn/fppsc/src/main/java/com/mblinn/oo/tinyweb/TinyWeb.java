package com.mblinn.oo.tinyweb;

import java.util.List;
import java.util.Map;

public class TinyWeb {
  private Map<String, Controller> controllers;
  private List<Filter> filters;

  public TinyWeb(Map<String, Controller> controllers, List<Filter> filters) {
    this.controllers = controllers;
    this.filters = filters;
  }

  public HttpResponse handleRequest(HttpRequest httpRequest) {
    HttpRequest currentRequest = httpRequest;
    for(Filter filter: filters) {
      currentRequest = filter.doFilter(currentRequest);
    }
    Controller controller = Controllers.get(currentRequest.getPath());
    if(null == controller)
      return null;
    return controller.handleRequest(currentRequest);
  }
}
