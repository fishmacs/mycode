package com.mblinn.oo.tinyweb;

import java.util.List;
import java.util.Map;

public abstract class TemplateController implements Controller {
  private View view;

  public TemplateController(View view) { this.view = view; }

  public HttpResponse handleRequest(HttpRequest httpRequest) {
    Integer responseCode = 200;
    String responseBody = "";

    try {
      Map<String, List<String>> model = doRequest(request);
    } catch(ControllerException e) {
      responseCode = e.getStatusCode();
    } catch(RenderingException e) {
      responseCode = 500;
      responseBody = "Exception while rendering.";
    } catch(Exception e) {
      responseCode = 500;
    }

    return HttpResponse.Builder.newBuilder().body(responseBody)
      .responseCode(responseCode).build();
  }

  protected abstract Map<String, List<String>> doRequest(HttpRequest request);
}
