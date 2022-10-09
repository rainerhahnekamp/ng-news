package com.rainerhahnekamp.news.web.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
@Data
@AllArgsConstructor
public class Episode {
    private Long id;
    private String name;
    private String content;
    private String imageSrc;
    public Episode() {}
}