package action;

import java.util.List;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.Namespace;
import org.apache.struts2.convention.annotation.ParentPackage;

import service.RemindService;
import util.JsonUtil;

@ParentPackage(value = "struts-default")
@Namespace(value = "/")
@Action(value = "remindAction", results = {})
public class RemindAction extends BaseAction {

	private RemindService remindService = new RemindService();

	public String remind() throws Exception {
		String inputWord = request.getParameter("word");
		List<String> wordList = null;
		String[] strs = inputWord.split(" +");
		String word = strs[strs.length - 1];
		if (inputWord.endsWith(" ")) {
			//该用户已经完整的输入了某个单词，并按下了空格
			wordList = remindService.getNextWordList(word);
		} else {
			//用户还未完整输入该单词
			wordList = remindService.getWordList(word);
		}
		String str = JsonUtil.objToStr(wordList);
		System.out.println(wordList);
		out.write(str);
		return null;
	}

	@Override
	public String execute() {
		// TODO Auto-generated method stub
		return null;
	}

}
