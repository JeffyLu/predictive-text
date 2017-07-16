package service;

import java.util.List;

import com.sun.org.apache.bcel.internal.generic.NEW;

import dao.RemindDao;

public class RemindService {

	private RemindDao remindDao = new RemindDao();

	public List<String> getWordList(String begin) {
		return remindDao.getWordList(begin);
	}

	public List<String> getNextWordList(String inputWord) {
		// TODO Auto-generated method stub
		return remindDao.getNextWordList(inputWord);
	}
}
