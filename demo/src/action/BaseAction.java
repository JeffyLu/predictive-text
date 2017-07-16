package action;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletContext;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.apache.struts2.interceptor.ServletRequestAware;
import org.apache.struts2.interceptor.ServletResponseAware;
import org.apache.struts2.util.ServletContextAware;

import com.opensymphony.xwork2.ActionSupport;

public abstract class BaseAction extends ActionSupport implements ServletContextAware, ServletRequestAware, ServletResponseAware {

	protected HttpSession session;
	protected HttpServletRequest request;
	protected HttpServletResponse response;
	protected ServletContext context;
	protected PrintWriter out;

	public void setServletResponse(HttpServletResponse response) {
		this.response = response;
		this.response.setContentType("text/html;charset=UTF-8");
		if (this.response != null) {
			try {
				this.out = this.response.getWriter();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public void setServletRequest(HttpServletRequest request) {
		this.request = request;
		if (request != null) {
			this.session = request.getSession();
		}
	}

	public void setServletContext(ServletContext context) {
		this.context = context;
	}

	public abstract String execute();
}
