package dao;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import util.DBUtil;

public class RemindDao {
	public List<String> getWordList(String begin) {
		List<String> wordList = new ArrayList<String>();
		String sql = "select * from words where value like '" + begin + "%' order by counts desc limit 9";
		Connection conn = null;
		Statement stmt = null;
		ResultSet rs = null;
		int i = 1;
		try {
			conn = DBUtil.getConn();
			stmt = conn.createStatement();
			rs = stmt.executeQuery(sql);
			while (rs.next()) {

				String word = rs.getString("value");
				wordList.add(i + ". " + word);
				i++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			DBUtil.closeResource(rs, stmt, conn);
		}
		return wordList;
	}

	public List<String> getNextWordList(String begin) {
		List<String> wordList = new ArrayList<String>();
		StringBuffer sql = new StringBuffer();
		sql.append(" SELECT `next_word`.`value`, `relations`.`counts` FROM `relations` ");
		sql.append(" LEFT JOIN `words` AS `next_word` ON `next_word`.`id` = `relations`.`next_wid_id` ");
		sql.append(" INNER JOIN `words` ON (`relations`.`wid_id` = `words`.`id`) ");
		sql.append(" WHERE `words`.`value` = '" + begin + "' ");
		sql.append(" ORDER BY `relations`.`counts` DESC LIMIT 9");
		Connection conn = null;
		Statement stmt = null;
		ResultSet rs = null;
		int i = 1;
		try {
			conn = DBUtil.getConn();
			stmt = conn.createStatement();
			rs = stmt.executeQuery(sql.toString());
			while (rs.next()) {
				String word = rs.getString("value");
				System.out.println(word);
				wordList.add(i + ". " + word);
				i++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			DBUtil.closeResource(rs, stmt, conn);
		}
		return wordList;
	}

	public static void main(String[] args) {
		// RemindDao dao = new RemindDao();
		// dao.getNextWordList("a");
		String str = "add  yy  eww xx   ddd";
		String[] s = str.split(" +");

		System.out.println(s[s.length - 1]);
	}
}
