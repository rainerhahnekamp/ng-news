package com.rainerhahnekamp.news.web.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
@Data
@AllArgsConstructor
public class Episode {

    public Episode() {}

    private Long id;
    private String name;
    private String content;
}