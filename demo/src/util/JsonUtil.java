package util;

import com.google.gson.Gson;

public class JsonUtil {
	private static Gson gson = new Gson();

	private JsonUtil() {

	}

	public static String objToStr(Object obj) {
		return gson.toJson(obj);
	}
}
