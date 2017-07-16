package entity;

public class Word {
	private Integer id;
	private String word;

	public Word() {
	}

	public Word(Integer id, String word) {
		this();
		this.id = id;
		this.word = word;
	}

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getWord() {
		return word;
	}

	public void setWord(String word) {
		this.word = word;
	}

}
